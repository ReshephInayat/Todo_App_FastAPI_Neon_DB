import { baseUrl } from "@/lib/const";
import { Todo } from "@/types/todo";
import Image from "next/image";
import DeleteTodo from "./DeleteTodo";

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
    <ul className="flex flex-col justify-center items-center">
      {data.map((item) => {
        return (
          <li
            key={item.id}
            className="text-white text-center text-xl py-2 bg-slate-800 mt-10 border border-solid border-white rounded-lg  flex items-center px-10"
          >
            <div className="">{item.content}</div>
            <DeleteTodo todo_id={item.id} />
          </li>
        );
      })}
      {data && data.length === 0 && (
        <div className="flex justify-center items-center pt-8 pb-2">
          <Image src={"/img.svg"} alt="add task" width={250} height={250} />
        </div>
      )}
    </ul>
  );
}
