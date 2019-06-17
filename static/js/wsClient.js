var oShowLog = document.getElementById("showLog");

// 建立socket连接，等待服务器“推送”数据，用回调函数更新图表
$(document).ready(function () {
    namespace = '/log';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    socket.on('server_response', function (res) {
        var logNode = document.createElement("p");
        logNode.innerText = res;
        oShowLog.appendChild(logNode);
        oShowLog.scrollTop = oShowLog.scrollHeight;
    });
});