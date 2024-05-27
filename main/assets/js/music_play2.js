        let player;
        let isPlaying = false;
        console.log("çalışıyor bu")
        function onYouTubeIframeAPIReady() {
            player = new YT.Player('player', {
                height: '0',
                width: '0',
                videoId: '8DQxBdHyGVg', // YouTube video ID
                events: {
                    'onReady': onPlayerReady
                }
            });
        }

        function onPlayerReady(event) {
            console.log("buton çalışıyor mu  bro")
            
            var playButtons = document.querySelectorAll(".playPauseButton");
            playButtons.forEach(function(button) {
                button.addEventListener("click", function(){
                    var musicId = this.getAttribute("data-music-id"); // data-music-id'yi al
                    console.log("Music ID:", musicId);
                    if (isPlaying) {
                        player.pauseVideo();
                        isPlaying = false;
                        document.getElementById('playPauseIcon').innerText = '▶️';
                        button.innerText= '▶️';
                    } else {
                        player.playVideo();
                        isPlaying = true;
                        document.getElementById('playPauseIcon').innerText = '⏸️';
                        button.innerText= '⏸️';
                    }
                });
            });
            

            // Next düğmesine tıklanması durumunda bir sonraki şarkıya geç
            document.getElementById('nextButton').addEventListener('click', function() {
                // Örnek olarak başka bir YouTube videosunun video ID'sini buraya ekleyin
                player.loadVideoById('ANOTHER_YOUTUBE_VIDEO_ID_HERE');
            });

            // Oynatıcı zamanını güncellemek için zamanlayıcıyı başlat
            setInterval(updateTimeDisplay, 1000);
        }

        // Oynatıcı zamanını güncelleyen fonksiyon
        function updateTimeDisplay() {
            const currentTime = player.getCurrentTime();
            const duration = player.getDuration();
            const currentTimeFormatted = formatTime(currentTime);
            const durationFormatted = formatTime(duration);
            document.getElementById('timeDisplay').innerText = `${currentTimeFormatted} / ${durationFormatted}`;
        }

        // Zamanı dakika:saniye biçimine dönüştüren yardımcı fonksiyon
        function formatTime(time) {
            const minutes = Math.floor(time / 60);
            const seconds = Math.floor(time % 60);
            return `${minutes < 10 ? '0' : ''}${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
        }