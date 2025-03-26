import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import Cookies from "js-cookie";
import { useRecruiter } from "@/Context/RecruiterContext";

const Logout = () => {
  const { setIsSigned } = useRecruiter();

  const handleClick = () => {
    setIsSigned(false);
    Cookies.remove("isSigned");
    window.location.href = "/auth/login";
  };
  return (
    <AlertDialog>
      <AlertDialogTrigger asChild className="size-full bg-transparent p-0">
        <div className="size-full">
          <h1 className="text-black">Logout</h1>
        </div>
      </AlertDialogTrigger>
      <AlertDialogContent className="bg-white">
        <AlertDialogHeader>
          <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
          <AlertDialogDescription className="text-black">
            Are you sure you want to log out? You will need to log in again to
            access your account.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel className="text-black dark:text-white">
            Cancel
          </AlertDialogCancel>
          <AlertDialogAction onClick={handleClick}>Continue</AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
};
export default Logout;
