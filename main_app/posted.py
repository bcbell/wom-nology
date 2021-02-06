from django.views.generic import CreateView, UpdateView, DeleteView


class PostedCreateView(CreateView):
    def form_valid(self, form):
        print('form_valid called')
        object= form.save(commit=False)
        object.posted_by=self.request.user
        object.save()
        return super(PostedCreateView, self).form_valid(form)

class PostedUpdatedView(UpdateView):
    def get(self):
        print('updated called')
        qs= super(PostedUpdatedView, self).get()
        return qs.filter(posted_by=self.request.user)

class PostedDeleteView(DeleteView):
    def get(self):
        print('delete  called')
        qs=super(PostedDeleteView, self).get()
        return qs.filter(posted_by=self.request.user)