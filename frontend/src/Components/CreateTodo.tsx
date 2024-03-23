"use client";
import { useState } from "react";
import { Flip, ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const CreateTodo = () => {
  const [Task, setTask] = useState("");

  const SubmitHandler = async (e: any) => {
    {
      if (!Task) {
        e.preventDefault();
        toast.error("Add Your Task!", {
          position: "top-center",
          autoClose: 5000,
          hideProgressBar: true,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: 0,
          theme: "colored",
          transition: Flip,
        });
      } else {
        const res = await fetch(`/api/todos`, {
          method: "POST",
          body: JSON.stringify({ content: Task }),
        });
        console.log(res);
      }
    }
  };
  return (
    <div>
      <div className="flex flex-col md:flex-row md:gap-5 justify-center items-center gap-2 ">
        <form
          className="flex gap-5 flex-col md:flex-row md:gap-2 items-center justify-center"
          onSubmit={SubmitHandler}
        >
          <input
            value={Task}
            onChange={(e) => {
              setTask(e.target.value);
            }}
            placeholder="Enter Your Task"
            className="w-full flex-wrap text-white bg-slate-900 p-4 rounded-sm focus:border-2 border-solid border-l-blue-500 border-r-cyan-500 border-t-cyan-500 border-b-blue-500 outline-none hover:bg-sky-950 transition duration-300"
          ></input>

          <button className='w-[40%] p-3 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-md text-md text-white hover:bg-gradient-to-r hover:from-cyan-600 hover:to-blue-800 hover:scale-105 transition duration-300"'>
            Add Task
          </button>
          <ToastContainer />
        </form>
      </div>
    </div>
  );
};

export default CreateTodo;
