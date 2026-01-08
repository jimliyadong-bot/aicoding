#!/bin/bash

# 审计日志与安全加固自测脚本

BASE_URL="http://localhost:8000"
TOKEN=""
ADMIN_USERNAME="${ADMIN_USERNAME:?ADMIN_USERNAME is required}"
ADMIN_PASSWORD="${ADMIN_PASSWORD:?ADMIN_PASSWORD is required}"
TEST_USER_PASSWORD="${TEST_USER_PASSWORD:?TEST_USER_PASSWORD is required}"

echo "========================================="
echo "审计日志与安全加固自测脚本"
echo "========================================="

# 1. 登录获取 token
echo ""
echo "[1/5] 测试登录..."
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/admin/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"${ADMIN_USERNAME}\",\"password\":\"${ADMIN_PASSWORD}\"}")

TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
  echo "❌ 登录失败"
  echo "响应: $LOGIN_RESPONSE"
  exit 1
else
  echo "✅ 登录成功"
  echo "Token: ${TOKEN:0:20}..."
fi

# 2. 测试登录限流
echo ""
echo "[2/5] 测试登录限流..."
echo "连续登录 6 次,第 6 次应该被限流..."

for i in {1..6}; do
  RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/admin/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"username":"test_user","password":"wrong_password"}')
  
  if echo "$RESPONSE" | grep -q "登录次数过多"; then
    echo "✅ 第 $i 次登录被限流"
    break
  else
    echo "第 $i 次登录: $(echo $RESPONSE | grep -o '"message":"[^"]*' | cut -d'"' -f4)"
  fi
  sleep 1
done

# 3. 创建用户(触发审计日志)
echo ""
echo "[3/5] 测试创建用户(触发审计日志)..."
CREATE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/admin/users" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username":"test_audit_user",
    "real_name":"测试用户",
    "password":"'"${TEST_USER_PASSWORD}"'",
    "status":1
  }')

if echo "$CREATE_RESPONSE" | grep -q '"code":200'; then
  echo "✅ 创建用户成功"
  USER_ID=$(echo $CREATE_RESPONSE | grep -o '"id":[0-9]*' | cut -d':' -f2)
  echo "用户ID: $USER_ID"
else
  echo "❌ 创建用户失败"
  echo "响应: $CREATE_RESPONSE"
fi

# 4. 更新用户(触发审计日志)
echo ""
echo "[4/5] 测试更新用户(触发审计日志)..."
if [ ! -z "$USER_ID" ]; then
  UPDATE_RESPONSE=$(curl -s -X PUT "$BASE_URL/api/v1/admin/users/$USER_ID" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
      "real_name":"测试用户(已修改)",
      "status":1
    }')
  
  if echo "$UPDATE_RESPONSE" | grep -q '"code":200'; then
    echo "✅ 更新用户成功"
  else
    echo "❌ 更新用户失败"
    echo "响应: $UPDATE_RESPONSE"
  fi
fi

# 5. 删除用户(触发审计日志)
echo ""
echo "[5/5] 测试删除用户(触发审计日志)..."
if [ ! -z "$USER_ID" ]; then
  DELETE_RESPONSE=$(curl -s -X DELETE "$BASE_URL/api/v1/admin/users/$USER_ID" \
    -H "Authorization: Bearer $TOKEN")
  
  if echo "$DELETE_RESPONSE" | grep -q '"code":200'; then
    echo "✅ 删除用户成功"
  else
    echo "❌ 删除用户失败"
    echo "响应: $DELETE_RESPONSE"
  fi
fi

echo ""
echo "========================================="
echo "测试完成!"
echo "========================================="
echo ""
echo "提示:"
echo "1. 查看审计日志: SELECT * FROM admin_audit_log ORDER BY created_at DESC LIMIT 10;"
echo "2. 查看 Redis 限流: redis-cli KEYS 'login_limit:*'"
echo "3. 等待 5 分钟后限流会自动解除"
