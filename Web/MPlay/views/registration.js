let Registration = {
    render: async () => {
        return `
        <div class="loginMain loginBorders">
        <form>
            <fieldset class="loginFieldset loginBorders">
                <legend class="legendText">Рэгістрацыя</legend>
                <label class="labelText loginLabelText" for="login">Email:</label>
                <input class="InputField" type="text" name="login" id="login" autocomplete="off" required/><br>

                <label class="labelText" for="password">Пароль:</label>
                <input class="InputField" type="password" name="password" id="password" required/><br>
                
                <label class="labelText" style="text-decoration: underline;" for="confPassword">Пароль:</label>
                <input class="InputField" style="margin-top: 20px;" type="password"  name="confPassword" id="confPassword" required/><br>

                <input class="loginPageButton registrationButton" id="regBtn" type="button" value="Зарэгiстравацца">
            </fieldset>
        </form> 
    </div>
        `
    },

    afterRender:() => {
        let status = true;

        document.querySelector('#regBtn').onclick = function() {
            if(document.querySelector('#login').value != '' && document.querySelector('#password').value != ''){
                if(document.querySelector('#password').value == document.querySelector('#confPassword').value){
                    const promise = auth.createUserWithEmailAndPassword(document.querySelector('#login').value, document.querySelector('#password').value);
                    Registration.addUser();
                    window.location.hash = '/welcome';
                    promise.catch(e => {
                        alert(e.message);
                    });
                        
                }
                else{
                    alert(`Паролі не супадаюць!`);
                }
            }
            else{
                alert(`Палі не могуць быць пустымі`);
            }
        }
    },

    addUser: async ()  => {
        auth.onAuthStateChanged(firebaseUser => {
            if(auth.currentUser)
            {
                db.ref('users/').on('value', function(snapshot) {
                    for(let i in snapshot.val()) // i - number, snapshot.val()[i].id - login
                    {
                        if(snapshot.val()[i].id == firebaseUser.email)
                        {
                            //console.log('exist');
                            return;
                        }
                    }
                    //console.log('add');
                    db.ref('users/' + `${firebaseUser.uid}`).update({
                        email: firebaseUser.email,
                    });
                });
            }
        });
    }
};
export default Registration;