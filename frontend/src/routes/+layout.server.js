import { redirect } from '@sveltejs/kit';

export async function load({ cookies, url }) {
    if (url.pathname == '/credentials') {
        return
    }
    
    const sessionid = cookies.get('sessionid');
    if (!sessionid) {
        // not logged in
        throw redirect(302, '/credentials');
    }

    // optionally, fetch the user profile here too
    return {
        // user: await getUserProfile(sessionid)
    };
}