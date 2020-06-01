import React, {useState, useEffect} from 'react';
import logo from './logo.svg';
import './App.css';
import {Link} from 'react-router-dom'

function ItemDetail({match}) {
   useEffect(() => {
       fetchItem();
       console.log(match)
   },[]);

   const [item, setItem] = useState({});
   
   const fetchItem = async () => {
       const fetchItem = await fetch(`https://fortniteapi.io/items/get?id=${match.params.id}`,{
        method: 'GET',
        headers: {  
          'Authorization': '648d4acf-5079556a-0606b36e-58867a4e',
        }
      })
       const item = await fetchItem.json();
       setItem(item.item)
       console.log(item)
   };

  return (
    <div>
      <h1>{item.name}</h1>
      <p>{item.description}</p>
    </div>
  );
}

export default ItemDetail;
