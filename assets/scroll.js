window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        scroll_bottom: function (n_clicks) {
            if (n_clicks > 0) {
                setTimeout(function () {
                    window.scrollTo({
                        top: document.documentElement.scrollHeight,
                        behavior: 'smooth'
                    });
                }, 100);
            }
            return window.dash_clientside.no_update;
        }
    }
});