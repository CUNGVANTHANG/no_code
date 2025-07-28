<?php
// Không còn xử lý POST ở đây, chỉ hiển thị giao diện
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Crawl Facebook Page Posts</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f6f9;
            display: flex;
            justify-content: center;
            padding-top: 50px;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .container h2 {
            text-align: center;
            color: #333;
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin-top: 8px;
            margin-bottom: 16px;
            border: 1px solid #ccc;
            border-radius: 6px;
            box-sizing: border-box;
        }
        button {
            background-color: #007bff;
            color: white;
            cursor: pointer;
            font-weight: bold;
            border: none;
        }
        button:hover {
            background-color: #0056b3;
        }
        .post {
            margin-top: 20px;
            padding: 15px;
            border: 1px solid #e1e1e1;
            border-radius: 8px;
            background-color: #fafafa;
        }
        .post img {
            max-width: 100%;
            margin-top: 10px;
            border-radius: 6px;
        }
        .error {
            color: red;
            font-weight: bold;
        }
        .data-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background: white;
        }
        .data-table th,
        .data-table td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
            vertical-align: top;
        }
        .data-table th {
            background-color: #007bff;
            color: white;
            font-weight: bold;
        }
        .data-table tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        .data-table tr:hover {
            background-color: #f5f5f5;
        }
        .post-link {
            color: #007bff;
            text-decoration: none;
            word-break: break-all;
        }
        .post-link:hover {
            text-decoration: underline;
        }
        .post-message {
            max-width: 300px;
            word-wrap: break-word;
            white-space: pre-line;
        }
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
            color: #007bff;
        }
        .loading.show {
            display: block;
        }
        #crawl-btn {
            position: relative;
        }
        #crawl-btn:disabled {
            background-color: #6c757d;
            cursor: not-allowed;
        }
    </style>
</head>
<body>
<div class="container">
    <h2>Crawl Facebook Page</h2>
    <form id="crawl-form">
        <label for="page_id">Page ID</label>
        <input type="text" id="page_id" name="page_id" placeholder="Nhập Page ID" required>

        <label for="limit">Số lượng bài viết</label>
        <input type="number" id="limit" name="limit" min="1" value="5">

        <button type="button" id="crawl-btn">Crawl Data</button>
    </form>

    <div class="loading" id="loading">
        <p>🔄 Đang tải dữ liệu từ Facebook...</p>
    </div>

    <div id="error-message" class="error" style="display: none;"></div>

    <div id="results-container"></div>
</div>


<script>
document.addEventListener('DOMContentLoaded', function() {
    const crawlBtn = document.getElementById('crawl-btn');
    const loading = document.getElementById('loading');
    const errorMessage = document.getElementById('error-message');
    const resultsContainer = document.getElementById('results-container');
    const pageIdInput = document.getElementById('page_id');
    const limitInput = document.getElementById('limit');

    crawlBtn.addEventListener('click', function() {
        const pageId = pageIdInput.value.trim();
        const limit = limitInput.value || 5;

        if (!pageId) {
            showError('Vui lòng nhập Page ID');
            return;
        }

        // Reset UI
        hideError();
        showLoading();
        disableButton();
        clearResults();

        // Gửi request tới API
        fetch('api.php', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                page_id: pageId,
                limit: parseInt(limit)
            })
        })
        .then(response => response.json())
        .then(data => {
            hideLoading();
            enableButton();
            
            if (data.error) {
                showError(data.error);
            } else if (data.success) {
                displayResults(data.data);
                console.log('Facebook API Results:', data.data);
            }
        })
        .catch(error => {
            hideLoading();
            enableButton();
            showError('Có lỗi xảy ra khi kết nối tới server: ' + error.message);
            console.error('Error:', error);
        });
    });

    function showLoading() {
        loading.classList.add('show');
    }

    function hideLoading() {
        loading.classList.remove('show');
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
    }

    function hideError() {
        errorMessage.style.display = 'none';
    }

    function disableButton() {
        crawlBtn.disabled = true;
        crawlBtn.textContent = 'Đang tải...';
    }

    function enableButton() {
        crawlBtn.disabled = false;
        crawlBtn.textContent = 'Crawl Data';
    }

    function clearResults() {
        resultsContainer.innerHTML = '';
    }

    function displayResults(posts) {
        if (!posts || posts.length === 0) {
            resultsContainer.innerHTML = '<p style="text-align: center; color: #666; padding: 20px;">Không có dữ liệu để hiển thị</p>';
            return;
        }

        let tableHTML = `
            <table class="data-table">
                <thead>
                    <tr>
                        <th>STT</th>
                        <th>ID Bài viết</th>
                        <th>Nội dung</th>
                        <th>Reactions</th>
                        <th>Comments</th>
                        <th>Link bài viết</th>
                    </tr>
                </thead>
                <tbody>
        `;

        posts.forEach((post, index) => {
            const reactions = post.reactions && post.reactions.summary ? post.reactions.summary.total_count || 0 : 0;
            const comments = post.comments ? (post.comments.summary ? post.comments.summary.total_count || 0 : post.comments.count || 0) : 0;
            
            tableHTML += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${escapeHtml(post.id || 'N/A')}</td>
                    <td class="post-message">${escapeHtml(post.message || '[Không có nội dung]')}</td>
                    <td>${reactions}</td>
                    <td>${comments}</td>
                    <td>
                        <a href="${post.permalink_url || '#'}" target="_blank" class="post-link">
                            Xem bài viết
                        </a>
                    </td>
                </tr>
            `;
        });

        tableHTML += `
                </tbody>
            </table>
        `;

        resultsContainer.innerHTML = tableHTML;
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
});
</script>
</body>
</html>
