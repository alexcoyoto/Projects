import Main from "./main.js";

let Header = {
    render: async linkArr => {
        return `
            <div class="headerLogoContainer">
                <a href="#/main">
                    <img class="headerLogo" src="images/logo.png" alt="mainLogo" />
                </a>
            </div>
            <div class="searchPlace" id="searchFormId">            
                <form class="seachForm">
                    <img class="searchLogo" src="images/searchLogo.png" alt="searchLogo" />
                    <input class="searchInput" id="searchInputId" type="search" placeholder="Пошук" autocomplete="off"/>
                </form>
            </div>
            <div class="addTrackButtonContainer">
                <input class="addTrackButton" type="button" value="Add track" onClick="window.location='#/add'">
            </div>
            <div class="loginPage">
                <a id="userPage" href="#/autorization">
                    <img class="userLogo" src="images/user.png" alt="userLogo" />
                </a>
                <a class="loginPageLink" id="userName" href="#/autorization">
                </a>
            </div>
        `
    },

    afterRender: async () => {
        auth.onAuthStateChanged(firebaseUser => {
            if(firebaseUser){
                document.querySelector('#userPage').href = '#/user';
                document.querySelector('#userName').innerHTML = `Выйсцi з ${firebaseUser.email}`;
            }
            else{
                document.querySelector('#userPage').href = '#/autorization';
                document.querySelector('#userName').innerHTML = `Уваход/Рэгістрацыя`;
            }        
            /*
            firebaseUser.updateProfile({
                liked: "Jane Q. User",
                listened: "11"
              }).then(function() {
                console.log(firebaseUser.liked);
              }).catch(function(error) {
                console.log('error');
              });
              */
        });
        document.querySelector('#userName').onclick = function() {
            if(document.querySelector('#userName').innerHTML != `Уваход/Рэгістрацыя`){
                auth.signOut();
            }
        }

        var inputField = document.querySelector('#searchInputId');
        inputField.addEventListener("keyup", function() {Main.find(inputField.value)});

        var inputFieldClicked = document.querySelector('#searchFormId');
        inputFieldClicked.addEventListener("click", function() {Main.find(inputFieldClicked.value)});
    }
};

export default Header;