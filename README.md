# EvilGetSeat  
## 这是YSU图书馆占座脚本的python版本  
## 原理  

图书馆的预约规则：

1.  预约开始时间与当前时间相差小于一小时时，其他人无法占这个座位。
2.  预约开始时间可以无限变更。

利用这两个规则，先预定一个座位然后用脚本一直更改预约开始时间，使其与当前时间之差小于一小时，这样除我以外所有人都不能占这个座位，即这个座位是我的，因为预约没有开始，所以这个座位不是我的，也就不会违规。
