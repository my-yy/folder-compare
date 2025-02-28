# 从旧版本升级
1. pull代码
2. 在项目根目录执行 `python migration.py`  来更新数据库字段设置
3. 正常启动项目即可 ` bash 1_run_flask.sh`




# 部署
1. 服务器端 clone 代码
2. `pip install -r requirements.txt`
3. 启动项目： ` bash 1_run_flask.sh`
4. 通过 `服务器ip:5001` 访问（需要在平台开放 开发机 的TCP 5001端口）



# 架构

前端：vue2 

后端：flask + sqlite

