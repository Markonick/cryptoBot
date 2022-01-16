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
import { IPortfolio } from '../../customTypes';

interface Column {
  id: 'asset' | 'free' | 'locked';
  label: string;
  minWidth?: number;
  align?: 'right';
  format?: (value: number) => string;
}

const minWidth = 100;

const columns: readonly Column[] = [
  { id: 'asset', label: 'asset', minWidth: minWidth },
  { id: 'free', label: 'free', minWidth: minWidth },
  {
    id: 'locked',
    label: 'locked',
    minWidth: minWidth,
    align: 'right',
  }
];

function createData(
  asset: string,
  free: number,
  locked: number,
) {
  return {
    asset,
    free,
    locked,
  };
};

export const PortfolioTable: React.FC = () => {
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(10);
  const [count, setCount] = React.useState<number>(10);
  const [portfolio, setPortfolio] = useState<IPortfolio>();

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  useEffect(() => {
    const fetchPortfolio = async () => {
      // const baseUrl = process.env.REACT_APP_BASE_URL;
      const baseUrl = 'http://localhost:8000';
      await axios.get<IPortfolio>(`${baseUrl}/portfolio`).then(response => {
        setPortfolio(response?.data);
      });
    };
    fetchPortfolio();
    console.log('INITIAL EFFECT')
  }, [])


  const rows = portfolio?.balances.map((asset) => {
    return createData(
      asset.asset,
      asset.free,
      asset.locked);
  });

  const table = <Paper sx={{ width: '95%', overflow: 'hidden', margin: "50px 50px 0px 50px" }}>
    <TableContainer sx={{ maxHeight: "80vh" }} >
      <Table stickyHeader  aria-label="sticky table" >
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
          {rows?.map((row) => {
              return (
                <TableRow hover role="checkbox" tabIndex={-1} key={row.asset}>
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
