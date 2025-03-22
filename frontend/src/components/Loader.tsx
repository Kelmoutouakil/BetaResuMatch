const Loader = () => {
    return (
      <div className="relative w-[15px] aspect-square animate-[scaleAnimation_1.5s_infinite_steps(2)]">
        <div className="absolute inset-0 rounded-full bg-black shadow-[26px_0] animate-[shadowAnimation_0.75s_infinite_linear_alternate]"></div>
        <div
          className="absolute inset-0 rounded-full bg-black animate-[rotateAnimation_0.75s_infinite_linear_alternate]"
          style={{ transform: "translateX(13px) rotate(0deg) translateX(13px)" }}
        ></div>
      </div>
    );
  };
  
  export default Loader;
  