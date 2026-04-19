<!-- Auto-mirrored from upstream `documentation-main/sys_man/BatchJobManagement.md`. Do not edit by hand; regenerate via `scripts/build_from_docs.py`. -->

# 批处理作业管理

针对某些特别耗时的任务，DolphinDB 支持批处理作业，在与常规交互作业独立的工作线程池中执行这些任务。批处理作业工作线程数的最大值是由配置参数
maxBatchJobWorker 设置的。如果批处理作业的数量超过了限制，新的批处理作业将会进入队列等待。批处理作业工作线程在闲置超过 60 秒后会自动销毁。

批处理作业的输出结果存于由配置参数 batchJobDir 指定的文件夹。如果没有指定，默认路径是
<HomeDir>/batchJobs。每个批处理作业产生两个文件夹：<job\_id>.msg 和 <
Job\_id>.obj，分别存储中间消息和返回对象。另外，当系统接收、开始和完成批处理作业时，每个批处理作业会向 <
BatchJobDir>/batchJob.log 添加三条信息。

## 相关函数

* submitJob(jobId,
  jobDesc, jobDef, args...)
* submitJobEx(jobId, jobDesc, priority, parallelism, jobDef,
  args...)

以上两个函数将批处理作业提交到本地节点，并且返回作业的 ID。其中，*jobDesc*
为可选参数，如果没有指定，函数名就是作业的描述。

如需将批处理作业提交到远程节点，可以使用以下函数：

* rpc
* remoteRun
* remoteRunWithCompression

* getJobStatus(jobId)：取得批处理作业的状态。
* [getRecentJobs([top])](../funcs/g/getRecentJobs.html)：取得本地节点上最近 N 个作业的状态。
* getJobMessage(jobId)：取得批处理作业返回的中间消息。
* getJobReturn(jobId)：取得批处理作业返回的对象。
* cancelJob(jobId)：取消已经提交但尚未完成的批处理作业。

## 例子

* 把作业提交到本地节点：

  ```
  def job1(n){
      s = 0
      for (x in 1 : n) {
          s += sum(sin rand(1.0, 100000000)-0.5)
          print("iteration" + x + " " + s)
      }
      return s
  };
  job1_ID=submitJob("job1_ID","", job1, 100);

  getJobStatus(job1_ID);
  ```

  | node | userID | jobId | jobDesc | receivedTime | startTime | endTime | errorMsg |
  | --- | --- | --- | --- | --- | --- | --- | --- |
  | local8848 | root | job1\_ID | job1 | 2018.06.16T10:44:34.066 | 2018.06.16T10:44:34.066 |  |  |

  在作业状态中，EndTime 是空的。这意味着作业还在执行中。作业完成后，就能在状态中看到 EndTime。

  ```
  getJobStatus(job1_ID);
  ```

  | node | userID | jobId | jobDesc | receivedTime | startTime | endTime | errorMsg |
  | --- | --- | --- | --- | --- | --- | --- | --- |
  | local8848 | root | job1\_ID | job1 | 2018.06.16T10:44:34.066 | 2018.06.16T10:44:34.066 | 2018.06.16T10:46:10.389 |  |

  ```
  getJobMessage(job1_ID);
  2018-06-16 10:44:34.066064 Start the job [job1_ID]: job1
  2018-06-16 10:44:35.377095 iteration 1 1412.431451
  2018-06-16 10:44:36.624907 iteration 2 2328.917258
  2018-06-16 10:44:37.577107 iteration 3 5491.651822
  2018-06-16 10:44:38.530187 iteration 4 6332.907608
  2018-06-16 10:44:39.488295 iteration 5 8404.393113
  ......
  2018-06-16 10:46:06.655519 iteration 95 -13124.624482
  2018-06-16 10:46:07.562855 iteration 96 -14878.269863
  2018-06-16 10:46:08.520555 iteration 97 -9842.451424
  2018-06-16 10:46:09.456576 iteration 98 -8149.660675
  2018-06-16 10:46:10.373218 iteration 99 -10639.329897
  2018-06-16 10:46:10.389147 The job is done.

  getJobReturn(job1_ID);
  // output
  -4291.91147
  ```
* 把作业提交到远程节点：

  使用 *rpc* 函数（"DFS\_NODE2" 与本地节点在同一集群）：

  ```
  def jobDemo(n){
      s = 0
      for (x in 1 : n) {
          s += sum(sin rand(1.0, 100000000)-0.5)
          print("iteration" + x + " " + s)
      }
      return s
  };

  rpc("DFS_NODE2", submitJob, "job1_1", "", job1{10});

  rpc("DFS_NODE2", getJobReturn, "jobDemo3")
  // output
  Output: -3426.577521
  ```

  使用 *remoteRun* 函数：

  ```
  conn = xdb("DFS_NODE2")
  conn.remoteRun(submitJob, "job1_2", "", job1, 10);

  conn.remoteRun(getJobReturn, "job1_2");
  // output
  Output: 4238.832005
  ```
