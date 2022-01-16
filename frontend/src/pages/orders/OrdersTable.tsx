import React, { useEffect, useState } from 'react';
import axios from "axios";
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import { IOrderResponse, IOrder } from '../../customTypes';
import { GetOrders } from '../../api/GetOrders';

interface Column {
  id: 'orderId' | 'symbolId' | 'value' | 'rsi' | 'previRsi' | 'createdAt' | 'clientOrderId' | 'transactTime' | 'price' | 'origQty' | 'executedQty' | 'cummulativeQuoteQty' | 'status' | 'timeInForce' | 'type' | 'side';
  label: string;
  minWidth?: number;
  align?: 'right';
  format?: (value: number) => string;
}

const minWidth = 100;

const columns: readonly Column[] = [
  { id: 'orderId', label: 'orderId', minWidth: minWidth },
  { id: 'symbolId', label: 'symboId', minWidth: minWidth },
  {
    id: 'value',
    label: 'value',
    minWidth: minWidth,
    align: 'right',
  },
  {
    id: 'rsi',
    label: 'rsi',
    minWidth: minWidth,
    align: 'right',
  },
  {
    id: 'previRsi',
    label: 'previRsi',
    minWidth: minWidth,
    align: 'right',
    format: (value: number) => value.toFixed(2),
  },
  {
    id: 'createdAt',
    label: 'createdAt',
    minWidth: minWidth,
    align: 'right',
  },
  {
    id: 'clientOrderId',
    label: 'clientOrderId',
    minWidth: minWidth,
    align: 'right',
  },
  {
    id: 'transactTime',
    label: 'transactTime',
    minWidth: minWidth,
    align: 'right',
  },
  {
    id: 'price',
    label: 'price',
    minWidth: minWidth,
    align: 'right',
    format: (value: number) => value.toFixed(2),
  },
  {
    id: 'origQty',
    label: 'origQty',
    minWidth: minWidth,
    align: 'right',
  },
  {
    id: 'executedQty',
    label: 'executedQty',
    minWidth: minWidth,
    align: 'right',
  },
  {
    id: 'cummulativeQuoteQty',
    label: 'cummulativeQuoteQty',
    minWidth: minWidth,
    align: 'right',
  },
  {
    id: 'status',
    label: 'status',
    minWidth: minWidth,
    align: 'right',
  },
  {
    id: 'timeInForce',
    label: 'timeInForce',
    minWidth: minWidth,
    align: 'right',
  },
  {
    id: 'type',
    label: 'type',
    minWidth: minWidth,
    align: 'right',
  },
  {
    id: 'side',
    label: 'side',
    minWidth: minWidth,
    align: 'right',
  },
];

function createData(
  symbolId: number,
  orderId: number,
  value: string,
  rsi: number,
  previRsi: number,
  createdAt: number,
  clientOrderId: number,
  transactTime: number,
  price: number,
  origQty: number,
  executedQty: number,
  cummulativeQuoteQty: number,
  status: string,
  timeInForce: string,
  type: string,
  side: string,
) {
  return {
    symbolId,
    orderId,
    value,
    rsi,
    previRsi,
    createdAt,
    clientOrderId,
    transactTime,
    price,
    origQty,
    executedQty,
    cummulativeQuoteQty,
    status,
    timeInForce,
    type,
    side,
  };
};

export const OrdersTable: React.FC = () => {
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(10);
  const [count, setCount] = React.useState<number>(10);
  const [orders, setOrders] = useState<IOrder[]>([]);

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  useEffect(() => {
    const fetchOrders = async () => {
      const baseUrl = 'http://localhost:8000';
      const params = { pageNumber: page, pageSize: rowsPerPage }
      await axios.get<IOrderResponse>(`${baseUrl}/orders`, { params }).then(response => {
        console.log(response?.data)
        setOrders(response?.data.orders);
        setCount(response?.data.count);
      });
    };
    fetchOrders();
    console.log('INITIAL EFFECT')
  }, [])

  useEffect(() => {
    const fetchOrders = async () => {
      const baseUrl = 'http://localhost:8000';
      const params = { pageNumber: page, pageSize: rowsPerPage }
      await axios.get<IOrderResponse>(`${baseUrl}/orders`, { params }).then(response => {
        console.log(response?.data)
        setOrders(response?.data.orders);
        setCount(response?.data.count);
      });
    };
    fetchOrders();
    console.log('PAGE EFFECT') 
  }, [page, rowsPerPage])

  const rows = orders.map((order) => {
    return createData(
      order.signalDetails.symbol_id,
      order.signalDetails.order_id,
      order.signalDetails.value,
      order.signalDetails.curr_rsi,
      order.signalDetails.prev_rsi,
      order.signalDetails.created_at,
      order.orderResponse.clientOrder_id,
      order.orderResponse.transactTime,
      order.orderResponse.price,
      order.orderResponse.origQty,
      order.orderResponse.executedQty,
      order.orderResponse.cummulativeQuoteQty,
      order.orderResponse.status,
      order.orderResponse.timeInForce,
      order.orderResponse.type,
      order.orderResponse.side);
  });

  console.log(rows)
  console.log(rowsPerPage)
  console.log(page)
  console.log(rows.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage))
  const table = <Paper sx={{ width: '95%', overflow: 'hidden', margin: "50px 50px 0px 50px" }}>
    <TableContainer>
      <Table aria-label="sticky table" >
        <TableHead>
          <TableRow >
            {columns.map((column) => (
              <TableCell
                key={column.id}
                align={column.align}
                style={{ minWidth: column.minWidth, }}
              >
                {column.label}
              </TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => {
              return (
                <TableRow hover role="checkbox" tabIndex={-1} key={row.orderId}>
                  {columns.map((column) => {
                    const value = row[column.id];
                    return (
                      <TableCell key={column.id} align={column.align} style={{ fontSize: 10, }}>
                        {column.format && typeof value === 'number'
                          ? column.format(value)
                          : value}
                      </TableCell>
                    );
                  })}
                </TableRow>
              );
            })}
        </TableBody>
      </Table>
    </TableContainer>
  </Paper>;

  const pagination =
    <TablePagination
      rowsPerPageOptions={[10, 25, 100]}
      component="div"
      count={count}
      rowsPerPage={rowsPerPage}
      page={page}
      onPageChange={handleChangePage}
      onRowsPerPageChange={handleChangeRowsPerPage}
    />;
  
  return (
    <div>
      {table}
      {pagination}
    </div>
  );
}
