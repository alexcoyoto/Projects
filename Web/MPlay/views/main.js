import Footer from "./footer.js";

var nowPlaying;
var pressedBtnResult = '';
var listenedList = '';
var containersNumber;

let Main = {
    render: () => { 
        return `
        <div class="indexPageMain" id="indexPage">
        <div class="leftSide">
        <div class="mainHeadline">
            <div class="musicSectionContainer">
               <h3 class="musicSectionName">
                    Зараз слухаюць
               </h3>
            </div>
        </div>
        <div class="musicListContainer">
            <ul class="musicList">
                ${Main.renderSide("first")}
            </ul>
        </div>
        </div>
        <div class="centerSide">
        <div class="mainHeadline">
            <div class="musicSectionContainer">
                <h3 class="musicSectionName">
                    Рэкамендацыі
                </h3>
            </div>
        </div>
        <div class="musicListContainer">
        <ul class="musicList">
        ${Main.renderSide("second")}
        </ul>
        </div>
        </div>
        <div class="rightSide">
        <div class="mainHeadline">
            <div class="musicSectionContainer">
                <h3 class="musicSectionName">
                    Навіны
                </h3>
            </div>
        </div>
        <div class="musicListContainer">
        <ul class="musicList">
        ${Main.renderSide("third")}
        </ul>
        </div>
        </div>
    </div>
        `;
    },

    renderSide: (side) =>{
        var result = '';
        db.ref('tracks/').on('value', function(snapshot) {
            containersNumber=snapshot.val().length;
            for(var i=snapshot.val().length-1;i>=0;i--)
            {
                //console.log(nowPlaying);
                var currId = snapshot.val()[i].id;
                var nowPlayingClass = '';
                    if(nowPlaying  == currId)
                        nowPlayingClass = ' trackContainerClicked';

                //console.log(snapshot.val()[i].name);
                if(snapshot.val()[i].type == side)
                {
                    result +=`
                    <li class="track" id="liId${currId}">
                    <div class="trackContainer${nowPlayingClass}" id="containerId${currId}">
                        <img class="albumImage" id="albumId${currId}" src="">
                        <div class="trackName">
                            <tag id="trackName${currId}" class="trackName">${snapshot.val()[i].name}</tag>
                           <div class="authorName" id="authorName${currId}">${snapshot.val()[i].author}</div>
                        </div>
                        <div class="trackButtons">
                                <input class="trackButton" id="trackButtonId${currId}" type="image" src="images/like.png">
                        </div>
                    </div>
                </li>
                `;
                } //${snapshot.val()[i].image}
            }    //
        });
        return result;
    },

    afterRender:  async() => {
        auth.onAuthStateChanged(firebaseUser => {    
            if(!document.querySelector("#containerId0") && firebaseUser)
                window.location.hash = '/user';
            else if (!document.querySelector("#containerId0") && !firebaseUser)
                window.location.hash = '/autorization';
        });
        //console.log(document.querySelector("#containerId0"));
        db.ref('users/').on('value', function(snapshot) {
                var pressedBtnResultCurr = `${snapshot.val()[auth.currentUser.uid].liked}`;
                        
        if(auth.currentUser && containersNumber){
            var pressedBtnResultSplit = pressedBtnResultCurr.split(';');
            if(pressedBtnResultSplit)
                for(var i=0;i<pressedBtnResultSplit.length;i++)
                {
                    var currBtn = document.querySelector(`#trackButtonId${pressedBtnResultSplit[i]}`);
                    //console.log(currBtn);
                    currBtn.src = 'http://127.0.0.1:5501/images/like_red.png';
                }
        }
        })

        document.querySelector("#indexPage").onclick = function(event) {
            var target = event.target;//.closest('.trackContainer');
            if(target.className == 'trackButton'){
                Main.likeButtonClicked(target, String(target.id.match(/\d+/)));
            }
            else{
                target = event.target.closest('.trackContainer');
                if(target)
                {
                    Main.listenedListAdd(String(target.id.match(/\d+/)));
                    Main.startPalying(target);
                }
            }
        };
    },

    likeButtonClicked: (target, buttonId) => {
        if(auth.currentUser)
        {
            //var currUserId = Main.getUserId();
            //console.log(target.src);
            var imgAdress = "http://127.0.0.1:5501/images/";
            target.src == `${imgAdress}like.png` ? target.src = `${imgAdress}like_red.png` : target.src = `${imgAdress}like.png`;
            if(target.src == `${imgAdress}like_red.png`)
            {
                console.log(auth.currentUser.uid);
                db.ref('users/').on('value', function(snapshot) {
                    if(snapshot.val()[auth.currentUser.uid].liked)
                        pressedBtnResult = `${snapshot.val()[auth.currentUser.uid].liked};${buttonId}`;
                    else
                        pressedBtnResult = `${buttonId}`;
                })
                setTimeout(Main.udpateUserDatabase, 500);
                }
            else
            {
                db.ref('users/').on('value', function(snapshot) {
                    var splitLiked = snapshot.val()[auth.currentUser.uid].liked.split(';');
                    pressedBtnResult = '';
                    for(var i=0; i<splitLiked.length;i++)
                    {
                        if(splitLiked[i] != buttonId)
                             pressedBtnResult += `${splitLiked[i]};`;
                    }
                });
                pressedBtnResult = pressedBtnResult.substring(0, pressedBtnResult.length - 1);
                setTimeout(Main.udpateUserDatabase, 500);
            }

        }
        else
            window.location.hash = '/autorization';
    },

    udpateUserDatabase: () => {                
        //console.log(pressedBtnResult);
        db.ref('users/' + auth.currentUser.uid).update({
            liked: `${pressedBtnResult}`
        });
    },

    listenedListAdd:(buttonId) =>{
        if(auth.currentUser)
        {

            db.ref('users/').on('value', function(snapshot) {
                if(snapshot.val()[auth.currentUser.uid].listened)
                    listenedList = `${snapshot.val()[auth.currentUser.uid].listened};${buttonId}`;
                else
                    listenedList= `${buttonId}`;
                var listenedListSplit = listenedList.split(';');

                var uniqueList = [];
                for (let str of listenedListSplit) {
                    if (!uniqueList.includes(str)) {
                        uniqueList.push(str);
                    }
                }

                if(uniqueList.length == 9)
                    uniqueList.shift();

                var fixedList = '';
                for(let j=0; j<uniqueList.length;j++)
                    fixedList += `${uniqueList[j]};`;
                listenedList = fixedList.substring(0, fixedList.length - 1);
            });
            setTimeout(Main.udpateListened, 500);
        }
    },

    udpateListened: () => {                
        //console.log(pressedBtnResult);
        db.ref('users/' + auth.currentUser.uid).update({
            listened: `${listenedList}`
        });
    },

    startPalying:  async(target) => {
        db.ref('tracks/').on('value', function(snapshot) {
            for(var i=snapshot.val().length-1;i>=0;i--)
            {
                document.querySelector(`#containerId${i}`).className = "trackContainer";
            }   
        });
        Footer.playTrack(target);
        nowPlaying = parseInt(target.id.match(/\d+/));
    },

    find: (value) =>{
        window.location.hash = '/main';
        var name;
        var author;
        var contSelector;
        //console.log(value);
        if(value == '' || value == undefined || value == ' '){
            for(var i = 0; i<containersNumber; i++)
            {
                contSelector = document.querySelector(`#liId${i}`);
                contSelector.style = 'display: flex;';
            }
            return;
        }
        value = value.toLowerCase();
        for(var i = 0; i<containersNumber; i++)
        {
            name = document.querySelector(`#trackName${i}`);
            author = document.querySelector(`#authorName${i}`);
            if(!name.innerHTML.toLowerCase().includes(value))
            {
                contSelector = document.querySelector(`#liId${i}`);
                contSelector.style = 'display: none;';
            }else{
                contSelector = document.querySelector(`#liId${i}`);
                contSelector.style = 'display: flex;';
            }
            if(author.innerHTML.toLowerCase().includes(value)){
                contSelector = document.querySelector(`#liId${i}`);
                contSelector.style = 'display: flex;'; 
            }

        }
        //console.log(author.innerHTML);
    }


    /*getUserId:() => {
        db.ref('users/').on('value', function(snapshot) {
            for(var i = 0; i<snapshot.val().length; i++)
            {
                if(snapshot.val()[i].id == auth.currentUser.email)
                {
                    console.log(i);
                    console.log(i.type);
                    return i;
                }     
            }
            return null;
        });
    }*/
};

export default Main;