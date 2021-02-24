$(function(){
    // HistoryAPIでブラウザバックを無効化(chromeは仕様上不可)
    history.pushState(null, null, null);
    $(window).on("popstate", function(){
        history.pushState(null, null, null);
    });
});
