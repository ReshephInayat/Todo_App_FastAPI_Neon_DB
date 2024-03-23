import CreateTodo from "@/Components/CreateTodo";
import TodoList from "@/Components/TodoList";
import Image from "next/image";

export default function Home() {
  return (
    <div className="w-full h-screen pb-32 bg-gray-800 selection:text-white  ">
      {/* Page Title */}
      <div className="flex justify-center items-center">
        <h1 className=" pt-32 pb-10 text-3xl md:text-5xl font-bold bg-gradient-to-r from-cyan-500 to-blue-500 inline-block text-transparent bg-clip-text">
          Todo List
        </h1>
      </div>

      <CreateTodo />
      <TodoList />
    </div>
  );
}
