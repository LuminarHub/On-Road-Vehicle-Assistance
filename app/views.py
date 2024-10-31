from django.shortcuts import render
from django.views.generic import *
from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import PasswordChangeView
# Create your views here.


class HomeView(TemplateView):
    template_name="home.html"

# class UserRegistrationView(CreateView):
#     model = User
#     form_class = UserRegistrationForm
#     template_name = 'user_register.html'
#     success_url = reverse_lazy('login')

#     def form_valid(self, form):
#         form.instance.role = 'user'
#         return super().form_valid(form)

# class MechanicRegistrationView(CreateView):
#     model = User
#     form_class = MechanicRegistrationForm
#     template_name = 'mechanic_register.html'
#     success_url = reverse_lazy('login')

#     def form_valid(self, form):
#         form.instance.role = 'mechanic'
#         return super().form_valid(form)

# class CarRenterRegistrationView(CreateView):
#     model = User
#     form_class = CarRenterRegistrationForm
#     template_name = 'car_renter_register.html'
#     success_url = reverse_lazy('login')

#     def form_valid(self, form):
#         form.instance.role = 'car_renter'
#         return super().form_valid(form)

class AdminRegistrationView(CreateView):
    model = User
    form_class = AdminRegistrationForm
    template_name = 'Admin_register.html'
    success_url = reverse_lazy('admin-login')

    def form_valid(self, form):
        # form.instance.role = form.cleaned_data['role']
        return super().form_valid(form)


class RegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.role = form.cleaned_data['role']
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.success_url



class AdminHomeView(TemplateView):
    template_name="admin_home.html"

class CarRenterHomeView(TemplateView):
    template_name="car_renter_home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile']=CarRenterProfile.objects.get(user=self.request.user.id)
        except CarRenterProfile.DoesNotExist:
            pass
        context

class UserHomeView(TemplateView):
    template_name="user_home.html"

class MechnaicHomeView(TemplateView):
    template_name="mechanic_home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile']=MechanicProfile.objects.get(user=self.request.user.id)
        except MechanicProfile.DoesNotExist:
            pass
        return context


class AdminLoginView(FormView):
    template_name = 'admin_login.html'
    form_class = LoginForm
    success_url = reverse_lazy('admin-home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.role == 'admin':
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Invalid username or password for admin.')
            return self.form_invalid(form)

    def get_success_url(self):
        return self.success_url

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            if user.role == 'mechanic':
                return redirect('mechanic_home')
            elif user.role == 'car_renter':
                return redirect('car_home')
            else:
                return redirect('user_home')
        return super().form_invalid(form)


def LogoutView(request,*args,**kwargs):
    logout(request)
    return redirect("home")  


class AddLocationView(CreateView):
    model=Location
    form_class=AddLocationForm
    template_name="add_location.html"
    success_url=reverse_lazy('add-locations')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loc']=Location.objects.all()
        return context

def locationdelete(request,**kwargs):
    id=kwargs.get('pk')
    loc=Location.objects.get(id=id)
    loc.delete()
    return redirect('add-locations')

class MechanicProfileAddView(CreateView):
    model = MechanicProfile
    form_class = MechanicProfileForm
    template_name = 'mechanic_profile_add.html'
    success_url = reverse_lazy('mechanic_home')

    # def get_object(self, queryset=None):
    #     return MechanicProfile.objects.filter(user=self.request.user).first()

    def form_valid(self, form):
        print("hii")
        form.instance.user = self.request.user
        return super().form_valid(form) 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['location']=Location.objects.all()
        mech=MechanicProfile.SPECIALIZATION_CHOICES
        print(mech)
        context['mech']=mech
        return context
    

class MechanicProfileDetailView(DetailView):
    model = MechanicProfile
    template_name = 'mechanic_profile_view.html'
    context_object_name = 'data'
    success_url = reverse_lazy('mechanic_home')

    def get_object(self, queryset=None):
        # Retrieve the MechanicProfile object for the current user
        try:
            return get_object_or_404(MechanicProfile, user=self.request.user)
        except:
            messages.error(self.request, "User has no User Profile, Complete Profile!!!.")
            return redirect('mechanic_home')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile']=MechanicProfile.objects.get(user=self.request.user.id)
            return context
        except MechanicProfile.DoesNotExist:
            pass
            return context


class PendingMechanicView(ListView):
    model = MechanicProfile
    template_name = 'pending_mechanics_list.html'  # Replace 'pending_mechanics_list.html' with your actual template name
    context_object_name = 'data'

    def get_queryset(self):
        return MechanicProfile.objects.filter(status='pending')
    

def approve_mechanic(request, pk):
    mechanic_profile = get_object_or_404(MechanicProfile, pk=pk)
    if request.method == 'POST':
        mechanic_profile.status = 'approved'
        mechanic_profile.save()
        return redirect('pending-list')  # Redirect to the pending list page
    return redirect('pending-list')

class MechanicprofileUpdateView(UpdateView):
    model = MechanicProfile
    form_class = MechanicProfileForm
    template_name = 'mechanic_profile_update.html'
    success_url = reverse_lazy('mechanic_home')

    def get_object(self, queryset=None):
        try:
            return MechanicProfile.objects.get(user=self.request.user)
        except:
            messages.error(self.request, "User has no User Profile, Complete Profile!!!.")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile']=MechanicProfile.objects.get(user=self.request.user.id)
        except MechanicProfile.DoesNotExist:
            pass
        return context


class UserProfileAddView(CreateView):
    # def get(self,request,*args,**kwargs):
    #     form=UserProfileForm()
    #     return render(request,"user_profile_add.html",{"form":form})
    
    # def post(self,request,*args,**kwargs):

    #     id=kwargs.get("pk")
    #     user_object=UserProfile.objects.get(user=id)
    #     print(user_object)
    #     form=UserProfile(request.POST,instance=user_object,files=request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return render(request,"user_home.html",{"form":form})
    #     else:
    #         return render(request,"user_home.html",{"form":form})




    model = UserProfile
    form_class = UserProfileForm
    template_name = 'user_profile_add.html'
    success_url = reverse_lazy('user_home')

    def get_object(self, queryset=None):
        return UserProfile.objects.filter(user=self.request.user).first()

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form) 
    

class UserProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'user_profile_view.html'
    context_object_name = 'data'

    def get_object(self, queryset=None):
        try:
            return get_object_or_404(UserProfile, user=self.request.user)
        except:
             messages.error(self.request, "User has no User Profile, Complete Profile!!!.")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile']=UserProfile.objects.get(user=self.request.user.id)
        except UserProfile.DoesNotExist:
           pass
        return context

    
class UserProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'user_profile_update.html'
    success_url = reverse_lazy('user_home')

    def get_object(self, queryset=None):
        return UserProfile.objects.get(user=self.request.user)
    
class ApprovedMechanicListView(TemplateView):
    template_name = 'approved_mechanic.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('search', '')
        
        if search_query:
            context['mechanics'] = MechanicProfile.objects.filter(
                status='approved',
                location__name__icontains=search_query  
            )
        else:
            context['mechanics'] = MechanicProfile.objects.filter(status='approved')
        context['search_query'] = search_query        
        return context

class ReqToMechanicCreateView(CreateView):
    model = ReqToMechanic
    form_class = ReqToMechanicForm
    template_name = 'create_req.html'
    success_url = reverse_lazy('user_requests')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['location']=Location.objects.all()
        return context
    def form_valid(self, form):
        try:
            mechanic_id = self.kwargs.get('mechanic_id')
            mechanic = MechanicProfile.objects.get(pk=mechanic_id)
            form.instance.mechanic = mechanic
            # form.instance.user = self.request.user.userprofile
            form.instance.user = self.request.user.user_profile
            form.instance.phone=self.request.user.user_profile.phone
            return super().form_valid(form)
        except:
            messages.error(self.request, "User has no User Profile, Complete Profile!!!.")
            return redirect('create_req',mechanic_id=mechanic_id)
       
    

class MechanicReqListView(ListView):
    model = ReqToMechanic
    template_name = 'mechanic_req_list.html'
    context_object_name = 'requests'

    def get_queryset(self):
        try:
            mechanic_profile = self.request.user.mechanic_profile
            return ReqToMechanic.objects.filter(mechanic=mechanic_profile).order_by('-datetime')
        except :
                messages.error(self.request, "User has no User Profile, Complete Profile!!!.")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile']=MechanicProfile.objects.get(user=self.request.user.id)
        except MechanicProfile.DoesNotExist:
            pass
        return context

    

def update_status(request, pk):
    req = get_object_or_404(ReqToMechanic, pk=pk)
    if request.method == 'POST':
        req.status = 'completed'
        req.save()
        return redirect('mechanic_requests')  # Redirect to the pending list page
    return redirect('mechanic_requests')



class UserRequestsListView(ListView):
    model = ReqToMechanic
    template_name = 'user_requests.html'
    context_object_name = 'user_requests'

    def get_queryset(self):
        try:
            return ReqToMechanic.objects.filter(user=self.request.user.user_profile).order_by('-datetime')
        except:
            messages.error(self.request, "User has no User Profile, Complete Profile!!!.")
            # return redirect('user_home')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile']=UserProfile.objects.get(user=self.request.user.id)
        except UserProfile.DoesNotExist:
            pass
        return context






class FeedBackCreateView(CreateView):
    model = FeedBack
    form_class = FeedBackForm
    template_name = 'feedback.html'
    # success_url = reverse_lazy('user_requests')

    def get_success_url(self,**kwargs):
        id=self.kwargs.get('pk')
        return reverse_lazy('feedback_form',kwargs={'pk':id})

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        id=self.kwargs.get('pk')
        print(id)
        req=ReqToMechanic.objects.get(id=id)
        feed=FeedBack.objects.filter(mechanic=req.mechanic)
        context['feed']=feed
        context['feedback']=FeedBack.options
        try:
            context['profile']=UserProfile.objects.get(user=self.request.user.id)
        except UserProfile.DoesNotExist:
            pass
        return context

        return context
    def form_valid(self, form):
        req_to_mechanic = get_object_or_404(ReqToMechanic, pk=self.kwargs['pk'])
        form.instance.user = self.request.user.user_profile
        form.instance.request = req_to_mechanic
        form.instance.mechanic_id = req_to_mechanic.mechanic.id
        return super().form_valid(form)
    
class FeedbackListView(ListView):
    model = FeedBack
    template_name = 'feedback_list.html'
    context_object_name = 'feedback_list'

    def get_queryset(self):
        try:
            mechanic_profile = self.request.user.mechanic_profile
            return FeedBack.objects.filter(mechanic=mechanic_profile)
        except :
               messages.error(self.request, "User has no User Profile, Complete Profile!!!.")
            #    return redirect('mechanic_home')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile']=MechanicProfile.objects.get(user=self.request.user.id)
        except MechanicProfile.DoesNotExist:
            pass
        return context



class BillPaymentCreateView(CreateView):
    model = Bill
    form_class = BillPaymentForm
    template_name = 'create_bill.html'
    success_url = reverse_lazy('mechanic_requests')

    def form_valid(self, form):
        req_id = self.kwargs['pk']
        req = get_object_or_404(ReqToMechanic, pk=req_id)
        form.instance.req = req
        form.instance.mechanic = req.mechanic
        form.instance.customer = req.user
        payment_amount = form.cleaned_data['payment']
        return super().form_valid(form)

class BillPaymentCreateView(CreateView):
    model = Bill
    form_class = BillPaymentForm
    template_name = 'create_bill.html'
    success_url = reverse_lazy('mechanic_requests')

    def form_valid(self, form):
        req_id = self.kwargs['pk']
        req = get_object_or_404(ReqToMechanic, pk=req_id)
        form.instance.req = req
        form.instance.mechanic = req.mechanic
        form.instance.customer = req.user
        req.status='Payment Pending'
        req.save()
        payment_amount = form.cleaned_data['payment']
        return super().form_valid(form)
    


def bil_payment(request, pk):
    req = get_object_or_404(ReqToMechanic, pk=pk)
    bill = get_object_or_404(Bill, req=req)
    
    if request.method == 'POST':
        bill.status = 'completed'
        bill.save()
        return redirect('payment')  # Redirect to the pending list page
    return redirect('user_requests')


class PaymentSuccessView(TemplateView):
    template_name="payment_success.html"




class CarRenterProfileCreateView(CreateView):
    model = CarRenterProfile
    form_class = CarRenterProfileForm
    template_name = 'car_renter_profile.html'
    success_url = reverse_lazy('car_home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class CarRenterProfileUpdateView(UpdateView):
    model = CarRenterProfile
    form_class = CarRenterProfileForm
    template_name = 'car_renter_profile_update.html'
    success_url = reverse_lazy('car_renter_profile_view')

    def get_object(self, queryset=None):
        return self.request.user.carrental_profile
    
class CarRenterProfileDetailView(DetailView):
    model = CarRenterProfile
    template_name = 'car_renter_profile_detail.html'
    context_object_name = 'data'

    def get_object(self, queryset=None):
        try:
           return self.request.user.carrental_profile
        except:
            messages.error(self.request, "User has no User Profile, Complete Profile!!!.")

    

class RentCarCreateView(CreateView):
    model = RentCar
    form_class = RentCarForm
    template_name = 'rent_car.html'
    success_url = reverse_lazy('rentcar_list')

    def form_valid(self, form):
        try:
            form.instance.owner = self.request.user.carrental_profile
            
            return super().form_valid(form)
        except:
            messages.error(self.request, "User has no User Profile, Complete Profile!!!.")
            return redirect('car_renter_profile',pk=self.request.user.id)


class RentCarUpdateView(UpdateView):
    model = RentCar
    form_class = RentCarForm
    template_name = 'rent_car_update.html'
    success_url = reverse_lazy('rentcar_list')
    context_object_name = 'data'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user.carrental_profile)
    
class UserRentCarListView(ListView):
    model = RentCar
    template_name = 'rentcar_list.html'
    context_object_name = 'rentcars'

    def get_queryset(self):
        try:
           return RentCar.objects.filter(owner=self.request.user.carrental_profile)
        except:
            messages.error(self.request, "User has no User Profile, Complete Profile!!!.")
            
    

class RentCarListView(ListView):
    model = RentCar
    template_name = 'rent_car_user_list.html'
    context_object_name = 'cars'

    def get_queryset(self):
        return RentCar.objects.filter(status='available')
    
class ReserveCarView(CreateView):
    model = CarReserve
    form_class = ReservationForm
    template_name = 'reserve_car.html'
    success_url = reverse_lazy('user_home')

    def form_valid(self, form):
        form.instance.customer = self.request.user.user_profile
        form.instance.car = RentCar.objects.get(pk=self.kwargs['pk'])
        form.instance.total_price = self.calculate_total_price(form.cleaned_data['start_date'], form.cleaned_data['end_date'], form.instance.car.price)

        # Update the status of the car to 'not available'
        form.instance.car.status = 'not_available'
        form.instance.car.save()

        return super().form_valid(form)

    def calculate_total_price(self, start_date, end_date, price_per_day):
        total_days = (end_date - start_date).days
        return total_days * price_per_day

# class ReservationDetailView(DetailView):
    # model = CarReserve
    # template_name = 'reservation_detail.html'
    # context_object_name = 'reservation'

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(customer=self.request.user.user_profile)


class UserReservationListView(ListView):
    model = CarReserve
    template_name = 'user_reservation_list.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        try:
            return CarReserve.objects.filter(customer=self.request.user.user_profile)
        except:
            messages.error(self.request, "User has no User Profile, Complete Profile!!!.")
    

def update_reservation(request, pk):
    reservation = get_object_or_404(CarReserve, pk=pk)
    if request.method == 'POST':
        reservation.checked_out = True
        reservation.save()
        car = reservation.car
        car.status = 'available'
        car.save()
    return redirect('user_reservation_list') 


class CarOwnerReservationsListView(ListView):
    model = CarReserve
    template_name = 'car_owner_reservations.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        # Filter reservations by cars owned by the current car owner
        owned_cars = RentCar.objects.filter(owner__user=self.request.user)
        return CarReserve.objects.filter(car__in=owned_cars)
    

class CustomPasswordChangeView(FormView):
    def get_template_names(self):
        if self.request.user.role == "admin":
            return ['change_password.html']
        elif self.request.user.role == "user":
            return ['user_changepassword.html']
        elif self.request.user.role == "mechanic":
            return ['mechanic_changepassword.html']
        else:
            return ['car_renter_changepassword.html']    
        
    form_class=ChangePasswordForm
    def post(self,request,*args,**kwargs):
        form_data=ChangePasswordForm(data=request.POST)
        if form_data.is_valid():
            current=form_data.cleaned_data.get("current_password")
            print(current)
            new=form_data.cleaned_data.get("new_password")
            confirm=form_data.cleaned_data.get("confirm_password")
            user=authenticate(request,username=request.user.username,password=current)
            print(user)
            if user:
                if new==confirm:
                    user.set_password(new)
                    user.save()
                    # messages.success(request,"password changed")
                    logout(request)
                    return redirect("login")
                else:
                    if self.request.user.role == "admin":
                        return redirect("admin-home")
                    elif self.request.user.role == "user":
                        return redirect("user_home")
                    elif self.request.user.role == "mechanic":
                        return redirect("mechanic_home")
                    else:
                        return redirect("car_home")
                    # messages.error(request,"password mismatches!")
                    # return redirect("change_password")
            else:
                # messages.error(request,"passsword incorrect!")
                return redirect("change_password")
        else:
            return render(request,"change_password.html",{"form":form_data})
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            if self.request.user.role == "user":
                context['profile']=UserProfile.objects.get(user=self.request.user.id)
            elif self.request.user.role == "mechanic":
                context['profile']=MechanicProfile.objects.get(user=self.request.user.id)
            else:
                context['profile']=CarRenterProfile.objects.get(user=self.request.user.id) 
        except:
            pass
        return context

# class CustomPasswordChangeView(PasswordChangeView):
#     def get_template_names(self):
#         if self.request.user.role == "admin":
#             return ['change_password.html']
#         elif self.request.user.role == "user":
#             return ['user_changepassword.html']
#         elif self.request.user.role == "mechanic":
#             return ['mechanic_changepassword.html']
#         else:
#             return ['car_renter_changepassword.html']

#     def get_success_url(self):
#         # if self.request.user.role == 'admin':
#         #     return reverse_lazy('admin-home')
#         # elif self.request.user.role == 'mechanic':
#         #     return reverse_lazy('mechanic_home')
#         # elif self.request.user.role == 'car_renter':
#         #     return reverse_lazy('car_home')
#         # else:
#         return reverse_lazy('logout')


def mechanic_search(request):
    if request.method == 'GET':
        form = MechanicSearchForm(request.GET)
        if form.is_valid():
            mechanic = form.cleaned_data.get('mechanic')
            print(mechanic)
            # services = MechanicProfile.objects.filter(name__icontains=mechanic)
            services = MechanicProfile.objects.filter(location__name__icontains=mechanic)
            print(services)
            if services:
                return render(request, 'search_results.html', {'mechanics': services})
            else:
                error_message = "No services found for the provided category"
                return render(request, 'search_results.html', {'form': form, 'error_message': error_message})
        else:
            error_message = "Invalid search criteria."
            return render(request, 'search_results.html', {'form': form, 'error_message': error_message})
    else:
        form = MechanicSearchForm()
        return render(request, 'search_results.html', {'form': form})    
    

class UserPaymentDetailsView(CreateView):
    model = UserPayment
    form_class = UserPaymentForm
    template_name = 'user_paybill.html'
    context_object_name = 'bill'
    
    def get_success_url(self):
        return reverse_lazy('payment')

    def get_context_data(self, **kwargs) :
        context= super().get_context_data(**kwargs)
        try:
            id=self.kwargs.get('pk')
            print(id)
            bill = ReqToMechanic.objects.get(id=id)
            context['req']=ReqToMechanic.objects.get(id=id)
            print(bill)
            context['bill']=Bill.objects.get(req=bill)
        
            context['userpayment']=UserPayment.objects.filter(req=bill.id,customer=self.request.user.id)
        except Bill.DoesNotExist:
            pass
        return context

    

    def form_valid(self, form):
        req_id = self.kwargs['pk']
        req = get_object_or_404(ReqToMechanic, pk=req_id)
        form.instance.req = req
        form.instance.mechanic = req.mechanic
        form.instance.customer = req.user
        req.status= 'completed'
        req.save()
        return super().form_valid(form)


class UserPaymentView(TemplateView):
    template_name='user_payment_details.html'
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        id=self.kwargs.get('pk')
        bill=ReqToMechanic.objects.get(id=id)
        context['data']=UserPayment.objects.get(req=bill)
        return context
    
    

class MechanicHistory(TemplateView):
    template_name='mechanic_history.html'
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        id=self.kwargs.get('pk')
        mech=MechanicProfile.objects.get(id=id)
        context['history']=ReqToMechanic.objects.filter(mechanic=mech.id,status="completed")
        return context
    
    
