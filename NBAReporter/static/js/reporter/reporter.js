$(function() {
    form = $("#form");

    $("#list").click(function () {
        console.log("List Data ...")
        form.attr('action', 'list');
        form.submit();
    });

    $("#download").click(function () {
        console.log("Download File ...")
        form.attr('action', 'download');
        form.submit();
    });

    $("#index").click(function () {
        console.log("Go to index ...")
        form.attr('action', 'index');
        form.submit();
    });
});