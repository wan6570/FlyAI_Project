// main.js
/*
document.getElementById('getSummonerBtn').addEventListener('click', () => {
    const summonerName = "SummonerName"; // 원하는 소환사 이름을 입력하세요.
    
    // Flask API 엔드포인트 URL
    const apiUrl = `http://localhost:5000/summoner/${summonerName}`;
    
    // API 요청 보내기
    fetch(apiUrl)
        .then((response) => {
            if (!response.ok) {
                throw new Error(`API 요청 실패: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            // API에서 반환한 데이터를 처리
            const summonerInfoDiv = document.getElementById('summonerInfo');
            summonerInfoDiv.innerHTML = JSON.stringify(data, null, 2);
        })
        .catch((error) => {
            console.error("에러 발생:", error);
        });
});
*/

// main.js

const getSummonerInfoBtn = document.getElementById('getSummonerInfo');
const summonerNameInput = document.getElementById('summonerName');
const summonerInfoDiv = document.getElementById('summonerInfo');

getSummonerInfoBtn.addEventListener('click', () => {
    const summonerName = summonerNameInput.value;
    if (!summonerName) {
        alert('Please enter a summoner name.');
        return;
    }

    fetch(`/summoner?summoner_name=${summonerName}`)
        .then((response) => {
            if (!response.ok) {
                throw new Error(`API request failed: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            summonerInfoDiv.innerHTML = JSON.stringify(data, null, 2);
        })
        .catch((error) => {
            console.error('Error:', error);
            summonerInfoDiv.innerHTML = 'An error occurred.';
        });
});
