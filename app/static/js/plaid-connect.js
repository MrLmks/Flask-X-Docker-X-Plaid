
document.getElementById('connect-bank').addEventListener('click', async (event) => {
const url = "http://localhost:5001/api/create_link_token"
try {
    const response = await fetch(url, 
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify( {client_user_id: "sandbox-user"} )
        });
        if (!response.ok){
            throw new Error(`Status: ${response.status}`);
        }
    const result = await response.json();
    const handler = Plaid.create(
    {
        token: result.link_token,
        onSuccess: async (public_token, metadata) => {
        const url = "http://localhost:5001/api/exchange_public_token"
        try {
            const response = await fetch (url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify( {public_token: public_token} )
            });
        } catch (error) {
            console.error(`Error: ${error}`);
            }
        }
    }
)
handler.open();
} catch (error) {
    console.error("Error during fetch");
}
});
