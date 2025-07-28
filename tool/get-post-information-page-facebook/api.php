<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

$accessToken = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);
    
    if (!$input || !isset($input['page_id'])) {
        echo json_encode(['error' => 'Page ID is required']);
        exit;
    }
    
    $pageId = $input['page_id'];
    $limit = $input['limit'] ?? 5;
    
    $apiUrl = "https://graph.facebook.com/v18.0/$pageId/posts?fields=id,message,permalink_url,comments,reactions.summary(true)&limit=$limit&access_token=$accessToken";
    
    $json = @file_get_contents($apiUrl);
    $data = json_decode($json, true);
    
    if (!$data || isset($data['error'])) {
        echo json_encode([
            'error' => isset($data['error']) ? $data['error']['message'] : 'Không thể kết nối tới Facebook API hoặc dữ liệu trả về không hợp lệ'
        ]);
    } else {
        echo json_encode([
            'success' => true,
            'data' => isset($data['data']) && is_array($data['data']) ? $data['data'] : []
        ]);
    }
} else {
    echo json_encode(['error' => 'Method not allowed']);
}
?>
