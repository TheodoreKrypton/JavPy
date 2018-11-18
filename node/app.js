function doProcess(str) {
    eval(str);
}
doProcess(str);
process.stdin.on('data', function (data) {
    doProcess(data);
});
