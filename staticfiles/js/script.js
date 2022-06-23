let dates = document.getElementsByClassName('date')
   Array.from(dates).forEach(element => {
     if ( new Date(element.textContent)  != "Invalid Date"){
      element.textContent = new Date(element.textContent).toLocaleTimeString().replace(":00","")
     }
   });

let data = document.getElementById("data").children

function filter(pattern){
    Array.from(data).forEach(leauges => {
        if (leauges.id != pattern){
            leauges.hidden = true
        }
        else{
            leauges.hidden = false
        }

    })
}
// google translation
function googleTranslateElementInit() {
    new google.translate.TranslateElement({pageLanguage: 'en'}, 'google_translate_element');
  }