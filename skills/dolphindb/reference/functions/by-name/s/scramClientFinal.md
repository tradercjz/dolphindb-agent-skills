# ------------------ SCRAM 模式登录 ------------------
if __name__ == "__main__":

    # 客户端发起认证
    client_data = client_initiate_authentication("user01")

    # 服务端处理首次请求
    server_response = server_handle_client_first(
        client_data["username"],
        client_data["client_nonce"]
    )

    password = "123456"

    # 客户端生成证明
    client_proof_data = client_generate_proof(
        "user01",
        password,
        server_response["salt"],
        server_response["iteration_count"],
        client_data["client_nonce"],
        server_response["combined_nonce"]
    )

    # 服务端验证并返回签名
    # auth_sessions[server_response["combined_nonce"]]["auth_message"] = client_proof_data["auth_message"]
    server_signature = server_handle_client_final(
        "user01",
        server_response["combined_nonce"],
        client_proof_data["client_proof"]
    )

    # 客户端验证服务端签名
    computed_server_sig = hmac.new(
        client_proof_data["server_key"],
        client_proof_data["auth_message"].encode(),
        hashlib.sha256
    ).digest()

    # 若匹配则认证成功
    assert server_signature == base64.b64encode(computed_server_sig).decode()
    print("SCRAM authentication succeeded!")

    # 查看当前会话与用户
    print(s.run("getCurrentSessionAndUser()"))
```
