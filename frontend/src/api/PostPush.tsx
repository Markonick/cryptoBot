import { useEffect, useState } from "react";
import { useRecoilValue } from "recoil";
import axios from "axios";

export const PostPush = (symbols: string[]) => {
    const [data, setData] = useState<string>();
    // const baseUrl = process.env.REACT_APP_BASE_URL;
    const baseUrl = 'http://localhost:8000';
    console.log('POST PUSH before effect')
    console.log(baseUrl)
    useEffect(() => {
        const postPush = async () => {
            console.log('awaiting POST PUSH axios')
            await axios.post<any>(`${baseUrl}/symbols`, symbols).then(response => {
                setData(response?.data);
            });
        };
        postPush();
    }, []);

    return (
        data
    );
}
