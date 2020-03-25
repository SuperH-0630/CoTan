function update_box(box, json) {
    box.innerHTML='';
    for (i of json){
        let y=document.createElement('option');
        y.text=String(i);
        y.value=String(i);
        box.add(y, null)
    }
}