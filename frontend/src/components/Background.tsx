const BackGround = ({ children }: { children: React.ReactNode }) => {
    return (
      <div className="w-screen h-screen bg-[#B3C8CF] relative overflow-hidden">
        <div className="star absolute left-[-400px] top-[100px] z-0"></div>
        <div className="absolute left-[-400px] top-[100px] size-[900px] backdrop-blur-3xl z-0"></div>
        <div className="star absolute right-[-400px] bottom-[100px] z-0"></div>
        <div className="absolute right-[-400px] bottom-[100px] size-[900px] backdrop-blur-3xl z-0"></div>
  
        <div className="relative z-10">{children}</div>
      </div>
    );
  };
  
  export default BackGround;
  