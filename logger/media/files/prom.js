const mentionName = ((recipient, sender) => {
    return new Promise((resolve, reject) => {
        if (recipient && sender){
            return resolve(`${recipient} ${sender} says Hi!`)
        }else {
            return resolve('Both recipients and sender must be provided')
       }
    })
})


const messageReader = ((message) => {
    return new Promise((resolve, reject) => {
        resolve(`Processing .... ${message}`)
    })
})

const send = async (recipient, sender) => {
    try{
    const sending = await mentionName(recipient, sender);
    const processed = await messageReader(sending);
    console.log(processed)
    }catch (err){
        console.log(err.message)
    }
}

send('kwame','lois')