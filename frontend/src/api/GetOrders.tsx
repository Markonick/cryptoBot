import { useEffect, useState } from "react";
import { useRecoilValue } from "recoil";
import axios from "axios";
import { IOrder } from "../customTypes";

export const GetOrders = () => {
  const [orders, setOrders] = useState<IOrder[]>([]);
  // const baseUrl = process.env.REACT_APP_BASE_URL;
  const baseUrl = 'http://localhost:8000';
  useEffect(() => {
    const fetchOrders = async () => {
      console.log('BEFORE FETCHING ORDERS')
      await axios.get<IOrder[]>(`${baseUrl}/orders`).then(response => {
        console.log(response?.data)
        setOrders(response?.data);
      });
    };
    fetchOrders();
  }, []);

  return (
    { orders }
  );
}
