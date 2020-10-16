let Add = {
    render: async () => {
        return `
        <div class="loginMain loginBorders">
        <form>
            <fieldset class="loginFieldset loginBorders">
                <legend class="legendText">Дадаць трэк</legend>

                <label class="labelText"for="name">Назва трэка:</label>
                <input class="InputField" id="name" type="text" name="name" autocomplete="off" required/><br>

                <label class="labelText" for="author">Выканаўца:</label>
                <input class="InputField" id="author" type="text" name="author" autocomplete="off" required/><br>

                <label class="labelText" for="image">Выява альбома:</label>
                <input class="FileProvider" id="image" type="file" name="image" accept=".jpg, .png, .jpeg" required/><br>

                <label class="labelText" for="mp3">mp3 файл:</label>
                <input class="FileProvider" id="mp3" type="file" name="mp3" accept=".mp3" required/><br>

                <label class="labelText" for="type">Спіс, у якi дадаць:</label>
                <select id="type" class="addSelector" name="type">
                    <option value="first">Зараз слухаюць</option>
                    <option value="second">Рэкамендацыі</option>
                    <option value="third">Навіны</option>
                </select>

                <input class="loginPageButton registrationButton" id="addBtn" type="button" value="Дадаць">
                <progress class="uploader" id="uploader" value="0" max = "100">0%<progress>
            </fieldset>
        </form> 
    </div>
        `;
    },
    
    afterRender: () => {
        auth.onAuthStateChanged(firebaseUser => {
            if(!firebaseUser)
                alert("Трэба аўтарызавацца, каб дадаваць трэкі"); 
        });

        var uploader = document.querySelector('#uploader');
        document.querySelector('#addBtn').addEventListener('click', (e) => {
           if(document.querySelector('#name').value != '' && document.querySelector('#author').value != ''
            && document.querySelector('#image').value != '' && document.querySelector('#mp3').value != ''){

                var currentId;
                db.ref('tracks/').on('value', function(snapshot){currentId = snapshot.val()[snapshot.val().length-1].id + 1;});

                var imageFile = document.querySelector('#image').files[0];
                var mp3File = document.querySelector('#mp3').files[0];

                var storageRefImage = firebase.storage().ref('images/'+ `${currentId}.jpg`);
                var imageTask = storageRefImage.put(imageFile);

                var storageRefMp3 = firebase.storage().ref('mp3/'+ `${currentId}.mp3`);
                var task = storageRefMp3.put(mp3File);

                task.on('state_changed', 
                    function progress(snapshot){
                        let percentage = (snapshot.bytesTransferred/
                        snapshot.totalBytes) * 100;
                        uploader.value = percentage;
                    },

                    function error(err){},
                    
                    function complete(){
                        imageTask.snapshot.ref.getDownloadURL().then(function(downloadURL) {
                            console.log('File available at', downloadURL);
                            db.ref('tracks/' + `${currentId}`).set({
                                id:currentId,
                                name: document.querySelector('#name').value,
                                author: document.querySelector('#author').value,
                                image: downloadURL,
                                mp3: 'mp3/'+ `${currentId}.mp3`,
                                type: document.querySelector('#type').value,
                            })
                            window.location.hash = '/main';
                            alert("Трэк паспяхова загрузіўся");});

                        //task.snapshot.ref.getDownloadURL().then(function(downloadURL) {
                            //console.log('File available at', downloadURL);});
                    }
                );
            }
            else{
            alert(`Палі не могуць быць пустымі`);
            }
        });                   
        //db.ref('tracks/').on('value', function(snapshot) {
            //console.log(snapshot.val().length);});
    }
};
export default Add;