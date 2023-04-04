

// document.getElementById('search-button').addEventListener("click", search)
document.getElementById('movie-search').addEventListener("keypress", ()=> search())

function search(key=null) {
    let keyword = document.getElementById('movie-search').value.toLowerCase();
    let shows = document.getElementsByClassName('col-sm');
    console.log(shows);
    for (let i=0;i<shows.length;i++){
        let html = shows[i].innerHTML.toLowerCase();
        if (html.includes(keyword)){
            shows[i].style.display = 'block';    
        } 
        else{
            shows[i].style.display = 'none';
        }
    }
}