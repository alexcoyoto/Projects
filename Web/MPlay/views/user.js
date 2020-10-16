import Footer from "./footer.js";
//var containersNumber;
var nowPlaying;
var containersNumber;
var pressedBtnResult = '';
var listenedList = '';
var containersNumber;

let User = {
    render:() => {
        return `
        <div class="userMain" id="indexPage">
        <div class="leftSideUser">
        <div class="mainHeadline">
            <div class="musicSectionContainer">
               <h3 class="musicSectionName">
                    Вам спадабалася
               </h3>
            </div>
        </div>
        <div class="musicListContainer">
            <ul class="musicList" id="leftUl">
                ${User.renderSide('liked')}
            </ul>
        </div>
        </div>
        <div class="rightSideUser">
        <div class="mainHeadline">
            <div class="musicSectionContainer">
                <h3 class="musicSectionName">
                    Вы слухалi
                </h3>
            </div>
        </div>
        <div class="musicListContainer">
            <ul class="musicList" id="rightUl">
            ${User.renderSide('listened')}
            </ul>
        </div>
        </div>
    </div>
        `;
    },

    renderSide: (value) =>{
        var result ='';
        var splitAll = '';
        db.ref('users/').on('value', function(snapshot) {
            if(auth.currentUser)
            {
                var listProperty;
                if(value == 'liked')
                    listProperty = snapshot.val()[auth.currentUser.uid].liked;
                else
                    listProperty = snapshot.val()[auth.currentUser.uid].listened;      
                splitAll = listProperty.split(';');
            }
        });
        db.ref('tracks/').on('value', function(snapshot) {
            containersNumber=snapshot.val().length;
            for(var i=splitAll.length-1; i>=0; i--)
            {
                var currId = splitAll[i];
                var trackId = snapshot.val()[currId].id;

                //console.log(snapshot.val()[i].name);
                if(value == 'liked'){
                    result +=`
                    <li class="track">
                    <div class="trackContainer" id="containerId${trackId}">
                        <img class="albumImage" id="albumId${trackId}" src=""> 
                        <div class="trackName" id="trackName${trackId}">
                            ${snapshot.val()[currId].name}
                           <div class="authorName" id="authorName${trackId}">${snapshot.val()[currId].author}</div>
                        </div>
                        <div class="trackButtons">
                                <input class="trackButton" id="trackButtonId${trackId}" type="image" src="images/like.png">
                        </div>
                    </div>
                </li>
                `;//${snapshot.val()[currId].image}
                }
                else{
                    result +=`
                    <li class="track">
                    <div class="trackContainer" id="containerId${trackId}">
                        <img class="albumImage" id="albumId${trackId}" src=""> 
                        <div class="trackName">
                            ${snapshot.val()[currId].name}
                           <div class="authorName"> ${snapshot.val()[currId].author} </div>
                        </div>
                    </div>
                </li>
                `;//${snapshot.val()[currId].image}
                }
            }
        });
        //console.log(likedResult);
        return result;
    },

    afterRender: async () => {
        User.renderCheck();

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
            if(target.className == 'trackButton'){ // !!
               User.likeButtonClicked(target, String(target.id.match(/\d+/)));
            }
            else{
                target = event.target.closest('.trackContainer');
                if(target)
                {
                    User.listenedListAdd(String(target.id.match(/\d+/)));
                    User.startPalying(target);
                   // User.addTrackUserPage(target);
                }
            }
        };
    },

    addTrackUserPage: (target) =>{
        db.ref('users/').on('value', function(snapshot) {
            var listenedList = snapshot.val()[auth.currentUser.uid].listened.split(';');
            for(let i=0; i<listenedList.length; i++)
            {
                if(listenedList[i] == String(target.id.match(/\d+/))){
                    console.log('exist');
                    return;
                }
            }
            var curId = String(target.id.match(/\d+/));
            var currTrackName = document.querySelector(`#trackName${curId}`).innerHTML;
            var container = document.createElement('li');
            container.innerHTML = `<li class="track"> \
            <div class="trackContainer" id="containerId${curId}">\
                <img class="albumImage" id="albumId${curId}" src=""> \
                <div class="trackName">\
                    ${currTrackName}\
                </div>\
            </div>\
        </li>`;
            document.querySelector(`#rightUl`).prepend(container);
        });
    },

    renderCheck: () =>{
        for(var i=0; i<=30; i++)
        {
        if(document.querySelector(`#containerId${i}`))
            return;
        }
        window.location.hash = '/welcome';
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
                setTimeout(User.udpateUserDatabase, 500);
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
                setTimeout(User.udpateUserDatabase, 500);
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
            setTimeout(User.udpateListened, 500);
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
};

export default User;