document.getElementById('admin-edit').addEventListener("change", () => {
    let ids = ['add-venue', 'edit-venue', 'delete-venue', 'add-show', 'edit-show', 'delete-show'];
    let dropDown = document.getElementById('admin-edit');
    for(let i=0;i<6;i++){
        if (dropDown.value == ids[i]){
            document.getElementById(ids[i]).style.display = 'block';
        }
        else{
            document.getElementById(ids[i]).style.display = 'none'; 
        }
    }
})
