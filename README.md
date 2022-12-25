# Cloud Store
## Cloud Deploy Overview
This is a full stack web application deployed on AWS.
![](https://tva1.sinaimg.cn/large/008vxvgGgy1h9d0u5080tj312g0u0q7z.jpg)
We put our built frontend to be hosted as a static website in s3 bucket. And we use cloudfront distribution to fasten content delivery. When clients access the website, all requests are send to the api gateway and routed to according microservices endpoints. These endpoints are elastic IPs and ports of EC2 instances or the domains of elastic beanstalk, which is a serverless platform. Order service, user service and product service and directly interact with the relational databases. Search service calls elastic search api to do fuzzy searching. User service calls byteplant api to validate user’s email. User service can emit an event to a SNS topic and SNS send messages to Lambda to enable third party oauth login. Product service can also emit an event to SNS to call Lambda to send emails by calling sendgrid api. 
In addition, S3 bucket and elastic beanstalks can be updated automatically through code pipeline that connected to our github repositories. Lastly we used Certificate Maneger and route 53 to add a custom domain to the cloudfront.
## Functions
### register
![image](https://github.com/youthtoday/cloud-store/blob/main/imgs/register.gif)

### login
![image](https://github.com/youthtoday/cloud-store/blob/main/imgs/login.gif)

### oauth login
![image](https://github.com/youthtoday/cloud-store/blob/main/imgs/oauth.gif)

### product
![image](https://github.com/youthtoday/cloud-store/blob/main/imgs/product.gif)

### search
![image](https://github.com/youthtoday/cloud-store/blob/main/imgs/search.gif)


### collection and cart
![image](https://github.com/youthtoday/cloud-store/blob/main/imgs/collection_cart.gif)

### order
![image](https://github.com/youthtoday/cloud-store/blob/main/imgs/order.gif)

### feedback
![image](https://github.com/youthtoday/cloud-store/blob/main/imgs/feedback.gif)
