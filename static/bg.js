class Circle {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.r = Math.random() * 10 ;
        this._mr = Math.random();
        this._mx = (Math.random() - 0.5) * 2;
        this._my = (Math.random() - 0.5) * 2 ;
        this.ax = 0;
        this.ay = 0;
    }

    drawCircle(ctx) {
        ctx.beginPath();  // 开始绘制
        ctx.arc(this.x, this.y, this.r, 0, 2 * Math.PI);  // 画弧线
        ctx.closePath();  // 结束绘制
        ctx.fillStyle = 'rgba(204, 204, 204, 0.3)';
        ctx.fill();
    }

    drawLine(ctx, _circle) {
        let dx = this.x - _circle.x;  // 差距
        let dy = this.y - _circle.y;  // 差距
        let d = Math.sqrt(dx * dx + dy * dy);  // 勾股距离
        if (d < 180) {
            ctx.beginPath();
            //开始一条路径，移动到位置 this.x,this.y。创建到达位置 _circle.x,_circle.y 的一条线：
            ctx.moveTo(this.x, this.y);   //起始点
            ctx.lineTo(_circle.x, _circle.y);   //终点
            ctx.closePath();
            ctx.strokeStyle = 'rgba(204, 204, 204, ' + String(1 - (d/180)) + ')';
            ctx.stroke();
        }
    }

    set_a(ax, ay){
        this.ax += ax;
        this.ax /= 2;
        this.ay += ay;
        this.ay /= 2;
    }

    set_a_first(){
        if (Math.abs(this._mx) > 3) {
            this.ax = 0;
            this._mx = (Math.random() - 0.5) * 2;
        }
        if (Math.abs(this._my) > 3) {
            this.ay = 0;
            this._my = (Math.random() - 0.5) * 2;
        }
    }

    move(w, h) {
        this._mx += this.ax;
        this._my += this.ay;

        this._mx = (this.x < w && this.x > 1) ? this._mx : (-this._mx);
        this._my = (this.y < h && this.y > 1) ? this._my : (-this._my);
        this._mr = (this.r < 10 && this.r > 1) ? this._mr : (-this._mr);
        this.x += this._mx / 2;
        this.y += this._my / 2;
        this.r += this._mr / 2;
        if (this.r <= 0){
            this._mr = -this._mr;
            this.r = -this.r;
        }
        }}

class currentCirle extends Circle {
    constructor(x, y) {
        super(x, y);
        this.r = 8;
        this.R = 30;
        this.rad = 0;
        this.circle = [];
    }

    add() {
        console.log('add');
        document.getElementsByTagName('title').item(0).innerHTML = 'loading...';
        this.circle.push('rgba(204, 204, 204, 0.8)');
    }

    remove() {
        console.log('remove');
        this.circle.shift();
        if (this.circle.length === 0){
            document.getElementsByTagName('title').item(0).innerHTML = 'Hello';
        }
    }

    drawLine(ctx, _circle) {
        let dx = this.x - _circle.x;  // 差距
        let dy = this.y - _circle.y;  // 差距
        let d = Math.sqrt(dx * dx + dy * dy);  // 勾股距离
        if (d < 180){
            ctx.beginPath();
            ctx.moveTo(this.x, this.y);   //起始点
            ctx.lineTo(_circle.x, _circle.y);   //终点
            ctx.closePath();
            ctx.strokeStyle = 'rgba(204, 0, 0, ' + String(1 - (d / 180)) + ')';
            ctx.stroke();
            _circle.set_a(dx / 1800, dy / 1800);
        }else{
            _circle.set_a_first()
        }
    }

    drawCircle(ctx) {
        let l = this.circle.length;
        for (let i of this.circle){
            let dx = this.R * Math.cos(this.rad);
            let dy = this.R * Math.sin(this.rad);
            ctx.beginPath();  // 开始绘制
            ctx.arc(this.x + dx, this.y + dy, this.r, 0, 2 * Math.PI);  // 画弧线
            ctx.closePath();  // 结束绘制
            ctx.fillStyle = i;
            ctx.fill();
            this.rad += 2 * Math.PI * (1 / l);
            if (this.rad >= 2 * Math.PI){
                this.rad -= 2 * Math.PI}
        }
        this.rad += Math.PI * (15 / 180);
    }
}
//更新页面用requestAnimationFrame替代setTimeout
window.requestAnimationFrame = window.requestAnimationFrame || window.mozRequestAnimationFrame || window.webkitRequestAnimationFrame || window.msRequestAnimationFrame;

let canvas = document.getElementById('canvas');
let ctx = canvas.getContext('2d');
let w = canvas.width = canvas.offsetWidth;
let h = canvas.height = canvas.offsetHeight;
let circles = [];
let current_circle = new currentCirle(0, 0);  // 鼠标位置
let update_times = 0;
let draw = function () {
    ctx.clearRect(0, 0, w, h);  // 清空
    for (let i = 0; i < circles.length; i++) {
        circles[i].move(w, h);
        circles[i].drawCircle(ctx);
        for (j = i + 1; j < circles.length; j++) {
            circles[i].drawLine(ctx, circles[j])
        }
    }
    if (current_circle.x) {
        current_circle.drawCircle(ctx);
        for (let k = 1; k < circles.length; k++) {
            current_circle.drawLine(ctx, circles[k])
        }
    }else{
        for (let k = 1; k < circles.length; k++) {
            current_circle.set_a_first()
        }
    }
    update_times += 1;
    if (update_times >= 100) {
        circles.push(new Circle(Math.random() * w, Math.random() * h));
        circles.shift();
        update_times = 0
    }
    requestAnimationFrame(draw)
};

let init = function (num) {
    for (var i = 0; i < num; i++) {
        circles.push(new Circle(Math.random() * w, Math.random() * h));
    }
    draw();
};
window.addEventListener('load', init(220));
window.onmousemove = function (e) {  // 鼠标进入范围
    // e = e || window.event;
    current_circle.x = e.clientX;
    current_circle.y = e.clientY;
};
window.onmouseout = function () {  // 鼠标移出反围
    current_circle.x = null;
    current_circle.y = null;

};