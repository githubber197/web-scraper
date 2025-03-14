document.getElementById('scraperForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const url = document.getElementById('url').value;
    const dataType = document.getElementById('dataType').value;
    const dataList = document.getElementById('dataList');
    
    dataList.innerHTML = "<li>Loading...</li>";

   const response = await fetch('http://127.0.0.1:5000/scrape', {

        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url, dataType })
    });

    const data = await response.json();
    dataList.innerHTML = "";

    if (data.success) {
        data.results.forEach((item, index) => {
            const listItem = document.createElement('li');
            listItem.textContent = `${index + 1}. ${item}`;
            dataList.appendChild(listItem);
        });
    } else {
        dataList.innerHTML = "<li>Error: " + data.error + "</li>";
    }
});
