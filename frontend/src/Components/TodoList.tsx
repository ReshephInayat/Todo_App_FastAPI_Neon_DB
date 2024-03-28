import { baseUrl } from "@/lib/const";
import { Todo } from "@/types/todo";
import Image from "next/image";
import DeleteTodo from "./DeleteTodo";
import UpdateTodo from "./UpdateTodo";

const getTodos = async (): Promise<Todo[]> => {
  const url = baseUrl();
  const res = await fetch(`${url}/todos`, {
    cache: "no-store",
    next: { tags: ["todos"] },
  });
  if (!res.ok) {
    throw new Error("Failed to get Todos");
  }
  // console.log(res);s
  return await res.json();
};

export default async function TodoList() {
  const data = await getTodos();

  return (
    <ul className="flex flex-col h-[100%] justify-center items-center ">
      {data.map((item) => (
        <li
          key={item.id}
          className="flex items-center justify-center w-1/3 bg-slate-800 rounded-lg border border-white text-white text-xl py-2 px-10 mt-10 "
        >
          <div className="flex-1">{item.content}</div>
          <DeleteTodo todo_id={item.id} />
          <UpdateTodo todoId={item.id} />
        </li>
      ))}
      {data && data.length === 0 && (
        <div className="flex justify-center items-center pt-8 pb-2">
          <Image src={"/img.svg"} alt="add task" width={250} height={250} />
        </div>
      )}
    </ul>
  );
}
