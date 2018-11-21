function doProcess(str) {
    eval(str);
}

process.stdin.on('data', function (data) {
    doProcess(data);
});
