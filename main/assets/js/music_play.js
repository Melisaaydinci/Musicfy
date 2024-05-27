        let player;
        let isPlaying = false;
        var footer = document.getElementById("mainFooter");
        console.log("footeri buldun mu",footer)
      
        function togglePlayPause(button, videoId) {
            var footer = document.getElementById("mainFooter");
            console.log("fonksiyon çalışıyor")
            if (currentVideoId !== videoId) {
                player.loadVideoById(videoId);
                currentVideoId = videoId;
            }
            
            if (isPlaying) {
                player.pauseVideo();
                footer.style.display = "none";
                isPlaying = false;
                document.getElementById('playPauseIcon').innerText = '▶️';
                button.innerText = '▶️';
            } else {
                player.playVideo();
                footer.style.display = "block";
                isPlaying = true;
                document.getElementById('playPauseIcon').innerText = '⏸️';
                button.innerText = '⏸️';
            }
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