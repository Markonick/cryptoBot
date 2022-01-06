import { useEffect, useState } from "react";
import { useRecoilValue } from "recoil";
import axios from "axios";

export const PostPush = () => {
    const [data, setData] = useState<string>();
    // const baseUrl = process.env.REACT_APP_BASE_URL;
    const baseUrl = 'http://localhost:8000';
    console.log('POST PUSH before effect')
    console.log(baseUrl)
    useEffect(() => {
        const postPush = async () => {
            console.log('awaiting POST PUSH axios')
            await axios.post<string>(`${baseUrl}/push?message=connect`).then(response => {
                setData(response?.data);
            });
        };
        postPush();
    }, []);

    return (
        data
    );
}
