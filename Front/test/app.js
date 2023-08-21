// CSV 대신 데이터 배열을 사용합니다.
const userData = [
    {
        summonerName: "장연석",
        championName: "Olaf",
        teamPosition: "TOP",
        KDA: "16.0, 5.0, 0.0"
        // 다른 사용자 데이터 추가
    },
    {
        summonerName: "test",
        championName: "다른 챔피언",
        teamPosition: "MID",
        KDA: "10.0, 2.0, 5.0"
        // 다른 사용자 데이터 추가
    }
    // 필요한 만큼 사용자 데이터를 추가하세요.
];

// CSV 파일을 파싱하고 검색을 수행하는 함수
function searchUser() {
    const username = document.getElementById("searchInput").value;

    // 배열에서 사용자 검색
    const foundUsers = userData.filter(user => user.summonerName === username);

    if (foundUsers.length > 0) {
        displayUserInfo(foundUsers);
    } else {
        displayUserInfo(null);
    }
}

// 사용자 정보를 HTML에 표시하는 함수
function displayUserInfo(users) {
    const userInfoElement = document.getElementById("userInfo");
    if (users && users.length > 0) {
        const userHTML = users.map(user => {
            return `<p>사용자명: ${user.summonerName}</p><p>챔피언: ${user.championName}</p><p>포지션: ${user.teamPosition}</p><p>KDA: ${user.KDA}</p>`;
        }).join("<hr>");
        userInfoElement.innerHTML = userHTML;
    } else {
        userInfoElement.innerHTML = "<p>사용자를 찾을 수 없습니다.</p>";
    }
}
