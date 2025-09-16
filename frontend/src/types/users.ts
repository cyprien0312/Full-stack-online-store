export interface User {
    id: number;
    email: string;
    name: string;
  }
  
  export interface UserList {
    items: User[];
    total: number;
    page: number;
    size: number;
  }