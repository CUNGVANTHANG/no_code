// Simple Bookmarklet script to convert YouTube Shorts to regular YouTube
// Usage: Create new bookmark, paste script into URL field

// Single line version
javascript:(function(){let u=window.location.href,m=u.match(/shorts\/([^?/]+)/);if(m)window.location.href=`https://www.youtube.com/watch?v=${m[1]}`;else alert("This website is not YouTube Shorts!");})();

// Basic version
javascript:(function() {
    let url = window.location.href;
    let match = url.match(/shorts\/([^?/]+)/);
    if (match) {
        let videoId = match[1];
        let newUrl = `https://www.youtube.com/watch?v=${videoId}`;
        window.location.href = newUrl;
    } else {
        alert("This website is not YouTube Shorts!");
    }
})();