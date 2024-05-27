        let player;
        let songStatus = '';

        function onYouTubeIframeAPIReady() {
            console.log("buraya giriyor musun")
            player = new YT.Player('player', {
                height: '0',
                width: '0',
                videoId: 'VCLxJd1d84s',
                playerVars: {
                    'playsinline': 1,
                    'autoplay': 1
                },
                events: {
                    'onReady': onPlayerReady,
                    'onStateChange': onPlayerStateChange
                }
            });
        }

        function onPlayerReady(event) {
            event.target.playVideo();
        }

        function onPlayerStateChange(event) {
            if (event.data == YT.PlayerState.PLAYING) {
                songStatus = 'play';
            } else if (event.data == YT.PlayerState.PAUSED) {
                songStatus = 'pause';
            }
        }

        function changeStatus() {
            if (songStatus === 'play') {
                player.pauseVideo();
                songStatus = 'pause';
            } else if (songStatus === 'pause') {
                player.playVideo();
                songStatus = 'play';
            }
        }

        document.getElementById('playButton').addEventListener('click', changeStatus);
    