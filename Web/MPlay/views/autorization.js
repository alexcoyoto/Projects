
let Autorization = {
    render: async () => {
        return `
        <div class="loginMain loginBorders">
        <form>
            <fieldset class="loginFieldset loginBorders">
                <legend class="legendText">Уваход</legend>
                <label class="labelText loginLabelText"for="login">Email:</label>
                <input class="InputField" id="fistInptId" type="text" name="login" id="login" autocomplete="off" required/><br>
                <label class="labelText" for="password">Пароль:</label>
                <input class="InputField" id="secondInptId" type="password" name="password" id="password" autocomplete="off" required/><br>
                <input class="loginPageButton" id="loginBtn" type="button" value="Увайсцi">
                <input class="loginPageButton" style="float: right;" type="button" value="Зарэгiстравацца" onClick="window.location='#/registration'">
            </fieldset>
        </form> 
    </div>
        `;
    },
    
    afterRender: async () => {
        auth.signOut();
        document.querySelector('#loginBtn').onclick = function() {
            if(document.querySelector('#fistInptId').value != '' && document.querySelector('#secondInptId').value != '')
            {
                auth.signInWithEmailAndPassword(document.querySelector('#fistInptId').value, document.querySelector('#secondInptId').value).then(() => {
                //alert(`Карыстач ${firebaseUser.email} паспяхова аўтарызаваўся`);
                window.location.hash = '/main';
                }).catch(e => {
                    status = false;
                    alert(e.message);
                });
            }
            else{
                alert(`Палі не могуць быць пустымі`);
            }
        }
    }
};
export default Autorization;