
import axios from "axios";
import firebase from "firebase";


const firebaseConfig = {
  apiKey: "AIzaSyDgfC6t3v4X63RCNv3Ye4l2TjKKlqxuVOs",
  authDomain: "kurva-14d74.firebaseapp.com",
  projectId: "kurva-14d74",
  storageBucket: "kurva-14d74.appspot.com",
  messagingSenderId: "1005440344669",
  appId: "1:1005440344669:web:c3b311f2fbcb6feaaba3b4",
  measurementId: "G-YJFN3VE72F",
};

firebase.initializeApp(firebaseConfig);

const database = firebase.database();

const form = document.getElementById("my-form");

form.addEventListener("submit", (e) => {
  e.preventDefault();

  const name = document.getElementById("name").value;
  const age = parseInt(document.getElementById("age").value);

  const user = {
    name,
    age,
  };

  database.ref("users").push(user);

  console.log("Данные отправлены!");
});