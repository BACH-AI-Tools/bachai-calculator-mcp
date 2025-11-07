#!/usr/bin/env python3
"""
测试计算器 MCP 服务器
"""

import subprocess
import json
import sys

def test_calculator():
    """测试计算器功能"""
    print("=" * 60)
    print("测试计算器 MCP 服务器")
    print("=" * 60)
    
    process = subprocess.Popen(
        [sys.executable, "main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    tests = [
        {
            "name": "初始化",
            "request": {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
        },
        {
            "name": "列出工具",
            "request": {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
        },
        {
            "name": "加法: 10 + 5",
            "request": {
                "jsonrpc": "2.0", "id": 3, "method": "tools/call",
                "params": {"name": "calculate", "arguments": {"operation": "add", "a": 10, "b": 5}}
            }
        },
        {
            "name": "乘法: 7 × 8",
            "request": {
                "jsonrpc": "2.0", "id": 4, "method": "tools/call",
                "params": {"name": "calculate", "arguments": {"operation": "multiply", "a": 7, "b": 8}}
            }
        },
        {
            "name": "平方根: √16",
            "request": {
                "jsonrpc": "2.0", "id": 5, "method": "tools/call",
                "params": {"name": "sqrt", "arguments": {"number": 16}}
            }
        },
        {
            "name": "阶乘: 5!",
            "request": {
                "jsonrpc": "2.0", "id": 6, "method": "tools/call",
                "params": {"name": "factorial", "arguments": {"number": 5}}
            }
        },
        {
            "name": "三角函数: sin(30°)",
            "request": {
                "jsonrpc": "2.0", "id": 7, "method": "tools/call",
                "params": {"name": "trigonometry", "arguments": {"function": "sin", "angle": 30}}
            }
        },
        {
            "name": "对数: log₁₀(100)",
            "request": {
                "jsonrpc": "2.0", "id": 8, "method": "tools/call",
                "params": {"name": "logarithm", "arguments": {"number": 100, "base": 10}}
            }
        }
    ]
    
    try:
        for test in tests:
            print(f"\n[测试] {test['name']}")
            
            process.stdin.write(json.dumps(test['request']) + "\n")
            process.stdin.flush()
            
            response_line = process.stdout.readline()
            
            if response_line:
                response = json.loads(response_line)
                
                if "result" in response:
                    print(f"✅ 成功")
                    
                    result = response['result']
                    if test['name'] == "初始化":
                        print(f"   服务器: {result.get('serverInfo')}")
                    elif test['name'] == "列出工具":
                        tools = result.get('tools', [])
                        print(f"   工具数量: {len(tools)}")
                        for tool in tools[:3]:
                            print(f"   - {tool['name']}")
                    else:
                        content = result.get('content', [])
                        if content:
                            print(f"   结果: {content[0].get('text', '')}")
                else:
                    print(f"❌ 失败")
                    print(f"   错误: {response.get('error')}")
            else:
                print(f"❌ 没有响应")
                
    except Exception as e:
        print(f"\n❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        process.terminate()
        process.wait()
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    test_calculator()

