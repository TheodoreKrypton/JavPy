function doProcess(str) {
    eval(str);
}

process.stdin.on('data', data => {
    doProcess(data);
});