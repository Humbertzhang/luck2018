# API Doc

HOST: http://39.108.79.110 <br>
PORT: 3500 <br>

URL | Header | Method
---- | --- | ---
/api/loginccnu/ | 无 | POST 

**`POST DATA`**

```
{
	"sid": "2016210000", //学号，类型string
	"password": "password" //密码，类型string
}
```



**`RESPONSE DATA`**

成功 <br>
`STATUS CODE = 200`<br>
```
{
	"name": "string", //名字
	"gender":"string",　//性别 男 or 女
	"college": "string" //学院
}
```

密码错误 <br>
`STATUS CODE = 401`<br>
```
{
	"msg":"failed"
}
```

未录入学校系统或发生其他错误<br>
`STATUS CODE = 404`<br>
```
{
	"name": "", //均为空字符串
	"gender": "",　//
	"college": "" //
}
```

JSON格式错误 (用于调试)<br>
`STATUS CODE = 400` <br>
```
{
	"msg":"JSON FORMAT ERROR"
}
```

