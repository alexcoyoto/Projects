
let Footer = {
    render: async linkArr => {
        return `
        <div class="playerContainer">
        <div class="trackInfo" id="trackInfo">
        
        </div>
        <audio class = "player" id="player"  controls>
        <source id = "source" src="" type="audio/mpeg">
        Тэг audio не падтрымваецца вашым браўзарам 
      </audio>
      </div>
        `
    },

    playTrack: async (target) =>{
        console.log(target.id);
        if(target)
        {
            var trackId = parseInt(target.id.match(/\d+/));
            db.ref('tracks/').on('value', function(snapshot){
                 //console.log(snapshot.val()[trackId].mp3);
                var storage = firebase.storage();
                var pathReference = storage.ref(snapshot.val()[trackId].mp3);
                target.className = target.className + " trackContainerClicked";
                pathReference.getDownloadURL().then(function(url) {

                    var mp3 = document.getElementById('player');
                    mp3.src = url;
                    mp3.play();
                    document.querySelector("#trackInfo").innerHTML = `${snapshot.val()[trackId].author} - ${snapshot.val()[trackId].name}`; 
                  }).catch(function(error) {
                  });
            });
        }
    },

    afterRender: async () => {
 
    }
};
export default Footer;
